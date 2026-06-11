from django import forms


class FreightForm(forms.Form):
    dollars = forms.FloatField(
        label='💰 Invoice Dollars',
        min_value=1.0,
        initial=18500.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_dollars',
            'placeholder': 'e.g. 18500.00',
            'step': '0.01',
        })
    )


class InvoiceFlagForm(forms.Form):
    invoice_quantity = forms.IntegerField(
        label='Invoice Quantity',
        min_value=1,
        initial=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_invoice_quantity',
            'placeholder': 'e.g. 50',
        })
    )
    freight = forms.FloatField(
        label='Freight Cost',
        min_value=0.0,
        initial=1.73,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_freight',
            'placeholder': 'e.g. 1.73',
            'step': '0.01',
        })
    )
    invoice_dollars = forms.FloatField(
        label='Invoice Dollars',
        min_value=1.0,
        initial=352.95,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_invoice_dollars',
            'placeholder': 'e.g. 352.95',
            'step': '0.01',
        })
    )
    total_item_quantity = forms.IntegerField(
        label='Total Item Quantity',
        min_value=1,
        initial=162,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_total_item_quantity',
            'placeholder': 'e.g. 162',
        })
    )
    total_item_dollars = forms.FloatField(
        label='Total Item Dollars',
        min_value=1.0,
        initial=2476.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_total_item_dollars',
            'placeholder': 'e.g. 2476.00',
            'step': '0.01',
        })
    )
