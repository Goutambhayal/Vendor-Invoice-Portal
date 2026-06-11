"""
retrain_invoice_flag.py
-----------------------
Retrains the invoice flag classifier using the local inventory.db database
and saves compatible pickle files to models/ for the current scikit-learn version.

Run from the project root:
    python retrain_invoice_flag.py
"""
import sqlite3
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH      = PROJECT_ROOT / "data" / "inventory.db"
MODEL_OUT    = PROJECT_ROOT / "models" / "predict_flag_invoice.pkl"
SCALER_OUT   = PROJECT_ROOT / "models" / "scaler.pkl"

FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars",
]
TARGET = "flag_invoice"

# ── Load data ────────────────────────────────────────────────────────────────
print(f"Connecting to {DB_PATH} …")
conn = sqlite3.connect(str(DB_PATH))

query = """
WITH purchase_agg AS (
    SELECT
        p.PONumber,
        COUNT(DISTINCT p.Brand)                                    AS total_brands,
        SUM(p.Quantity)                                            AS total_item_quantity,
        SUM(p.Dollars)                                             AS total_item_dollars,
        AVG(julianday(p.ReceivingDate) - julianday(p.PODate))      AS avg_receiving_delay
    FROM purchases p
    GROUP BY p.PONumber
)
SELECT
    vi.PONumber,
    vi.Quantity  AS invoice_quantity,
    vi.Dollars   AS invoice_dollars,
    vi.Freight,
    pa.total_item_quantity,
    pa.total_item_dollars,
    pa.avg_receiving_delay
FROM vendor_invoice vi
LEFT JOIN purchase_agg pa
    ON vi.PONumber = pa.PONumber
"""

df = pd.read_sql_query(query, conn)
conn.close()
print(f"Loaded {len(df):,} rows.")

# ── Create label ─────────────────────────────────────────────────────────────
def create_label(row):
    if abs(row["invoice_dollars"] - row["total_item_dollars"]) > 5:
        return 1
    if row["avg_receiving_delay"] > 10:
        return 1
    return 0

df[TARGET] = df.apply(create_label, axis=1)
df = df.dropna(subset=FEATURES + [TARGET])

print(f"Label distribution:\n{df[TARGET].value_counts()}")

# ── Split ────────────────────────────────────────────────────────────────────
X = df[FEATURES]
y = df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Scale ────────────────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── Train (fast but accurate) ────────────────────────────────────────────────
print("Training RandomForestClassifier …")
clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=3,
    min_samples_leaf=2,
    criterion="gini",
    random_state=42,
    n_jobs=-1,
)
clf.fit(X_train_sc, y_train)

# ── Evaluate ─────────────────────────────────────────────────────────────────
preds = clf.predict(X_test_sc)
print(f"\nAccuracy: {accuracy_score(y_test, preds):.4f}")
print(classification_report(y_test, preds))

# ── Save ─────────────────────────────────────────────────────────────────────
joblib.dump(clf,    str(MODEL_OUT))
joblib.dump(scaler, str(SCALER_OUT))
print(f"\nSaved model  → {MODEL_OUT}")
print(f"Saved scaler → {SCALER_OUT}")
print("Done! Restart the Django server and test invoice flag prediction.")
