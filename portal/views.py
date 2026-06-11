import sys
import os
from pathlib import Path

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

# Add the project root to sys.path so inference modules can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from portal.forms import FreightForm, InvoiceFlagForm
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag


def home(request):
    """Redirect root URL to freight cost prediction."""
    return redirect('freight')


@require_http_methods(["GET", "POST"])
def freight_view(request):
    """
    Freight Cost Prediction page.
    GET  → render empty form
    POST → run inference and display result
    """
    prediction = None
    error = None
    form = FreightForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                dollars = form.cleaned_data['dollars']
                input_data = {"Dollars": [dollars]}
                result = predict_freight_cost(input_data)
                prediction = result['Predicted_Freight'][0]
            except Exception as e:
                error = f"Prediction error: {str(e)}"

    context = {
        'form': form,
        'prediction': prediction,
        'error': error,
        'active_page': 'freight',
    }
    return render(request, 'portal/freight.html', context)


@require_http_methods(["GET", "POST"])
def invoice_flag_view(request):
    """
    Invoice Manual Approval Flag prediction page.
    GET  → render empty form
    POST → run inference and display result
    """
    flag_result = None
    is_flagged = None
    error = None
    form = InvoiceFlagForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                cd = form.cleaned_data
                input_data = {
                    "invoice_quantity": [cd['invoice_quantity']],
                    "invoice_dollars":  [cd['invoice_dollars']],
                    "Freight":          [cd['freight']],
                    "total_item_quantity": [cd['total_item_quantity']],
                    "total_item_dollars":  [cd['total_item_dollars']],
                }
                result = predict_invoice_flag(input_data)
                flag_value = result['Predicted_Flag'][0]
                is_flagged = bool(flag_value)
                flag_result = True
            except Exception as e:
                error = f"Prediction error: {str(e)}"

    context = {
        'form': form,
        'flag_result': flag_result,
        'is_flagged': is_flagged,
        'error': error,
        'active_page': 'invoice_flag',
    }
    return render(request, 'portal/invoice_flag.html', context)
