from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import InventoryCategory, InventoryItem, PurchaseOrder


class InventoryCategoryForm(forms.ModelForm):
    class Meta:
        model = InventoryCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Div(
                Submit('submit', 'Save Category', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'item_type', 'quantity', 'unit', 'unit_price',
                  'reorder_level', 'location', 'is_active']
        widgets = {
            'location': forms.TextInput(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('category', css_class='col-md-6'),
            ),
            Row(
                Column('item_type', css_class='col-md-4'),
                Column('quantity', css_class='col-md-4'),
                Column('unit', css_class='col-md-4'),
            ),
            Row(
                Column('unit_price', css_class='col-md-4'),
                Column('reorder_level', css_class='col-md-4'),
                Column('location', css_class='col-md-4'),
            ),
            'is_active',
            Div(
                Submit('submit', 'Save Item', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['item', 'supplier_name', 'quantity', 'total_cost', 'order_date',
                  'expected_delivery', 'status']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('item', css_class='col-md-6'),
                Column('supplier_name', css_class='col-md-6'),
            ),
            Row(
                Column('quantity', css_class='col-md-4'),
                Column('total_cost', css_class='col-md-4'),
                Column('status', css_class='col-md-4'),
            ),
            Row(
                Column('order_date', css_class='col-md-6'),
                Column('expected_delivery', css_class='col-md-6'),
            ),
            Div(
                Submit('submit', 'Save Purchase Order', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
