from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Invoice, InvoiceItem, Payment


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['patient', 'appointment', 'discount', 'tax', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('appointment', css_class='col-md-6'),
            ),
            Row(
                Column('discount', css_class='col-md-6'),
                Column('tax', css_class='col-md-6'),
            ),
            'notes',
            Div(
                Submit('submit', 'Save Invoice', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('description', css_class='col-md-5'),
                Column('quantity', css_class='col-md-3'),
                Column('unit_price', css_class='col-md-4'),
            ),
            Div(
                Submit('submit', 'Add Item', css_class='btn btn-success'),
                css_class='mt-3'
            )
        )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('amount', css_class='col-md-6'),
                Column('payment_method', css_class='col-md-6'),
            ),
            'transaction_id',
            'notes',
            Div(
                Submit('submit', 'Record Payment', css_class='btn btn-success'),
                css_class='mt-3'
            )
        )


class InvoiceFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All')] + Invoice.STATUS_CHOICES
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search invoice...'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('search', css_class='col-md-8'),
                Column('status', css_class='col-md-4'),
            ),
            Div(
                Submit('submit', 'Filter', css_class='btn btn-primary btn-sm'),
                css_class='mt-2'
            )
        )
