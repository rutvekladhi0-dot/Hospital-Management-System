from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Supplier, Medicine, MedicineCategory, Prescription, PrescriptionItem, DispensedMedicine


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('contact_person', css_class='col-md-6'),
            ),
            Row(
                Column('phone', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            'address',
            'is_active',
            Div(
                Submit('submit', 'Save Supplier', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'category', 'category_fk', 'manufacturer',
                  'unit_price', 'stock_quantity', 'minimum_stock', 'expiry_date',
                  'batch_number', 'suppliers', 'is_active']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'suppliers': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('generic_name', css_class='col-md-6'),
            ),
            Row(
                Column('category', css_class='col-md-4'),
                Column('category_fk', css_class='col-md-4'),
                Column('manufacturer', css_class='col-md-4'),
            ),
            Row(
                Column('unit_price', css_class='col-md-4'),
                Column('stock_quantity', css_class='col-md-4'),
                Column('minimum_stock', css_class='col-md-4'),
            ),
            Row(
                Column('expiry_date', css_class='col-md-6'),
                Column('batch_number', css_class='col-md-6'),
            ),
            'suppliers',
            'is_active',
            Div(
                Submit('submit', 'Save Medicine', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicineCategory
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


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['visit', 'patient', 'diagnosis', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('visit', css_class='col-md-6'),
                Column('patient', css_class='col-md-6'),
            ),
            'diagnosis',
            'notes',
            Div(
                Submit('submit', 'Save Prescription', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine', 'dosage', 'frequency', 'duration', 'quantity', 'instructions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('medicine', css_class='col-md-6'),
                Column('dosage', css_class='col-md-6'),
            ),
            Row(
                Column('frequency', css_class='col-md-4'),
                Column('duration', css_class='col-md-4'),
                Column('quantity', css_class='col-md-4'),
            ),
            'instructions',
            Div(
                Submit('submit', 'Add Item', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class DispenseForm(forms.Form):
    prescription = forms.ModelChoiceField(queryset=Prescription.objects.filter(is_dispensed=False))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'prescription',
            'notes',
            Div(
                Submit('submit', 'Dispense Medicine', css_class='btn btn-success'),
                css_class='mt-3'
            )
        )
