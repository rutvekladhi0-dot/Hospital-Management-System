from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import LabTest, LabOrder, LabOrderItem, LabResult


class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['name', 'description', 'department', 'price', 'normal_range', 'unit', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('department', css_class='col-md-6'),
            ),
            'description',
            Row(
                Column('price', css_class='col-md-4'),
                Column('normal_range', css_class='col-md-4'),
                Column('unit', css_class='col-md-4'),
            ),
            'is_active',
            Div(
                Submit('submit', 'Save Test', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class LabOrderForm(forms.ModelForm):
    test_ids = forms.ModelMultipleChoiceField(
        queryset=LabTest.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(),
        label='Select Tests'
    )

    class Meta:
        model = LabOrder
        fields = ['patient', 'appointment', 'priority']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('appointment', css_class='col-md-6'),
            ),
            'priority',
            'test_ids',
            Div(
                Submit('submit', 'Create Lab Order', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )

    def save(self, commit=True):
        order = super().save(commit=False)
        order.doctor = self.instance.doctor if hasattr(self.instance, 'doctor') else None
        if commit:
            order.save()
            test_ids = self.cleaned_data['test_ids']
            for test in test_ids:
                LabOrderItem.objects.create(order=order, test=test)
        return order


class LabOrderItemForm(forms.ModelForm):
    class Meta:
        model = LabOrderItem
        fields = ['test', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'test',
            'notes',
            Div(
                Submit('submit', 'Add Test', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['result_value', 'reference_range', 'is_abnormal', 'notes', 'report_file']
        widgets = {
            'result_value': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'result_value',
            Row(
                Column('reference_range', css_class='col-md-6'),
                Column('is_abnormal', css_class='col-md-6'),
            ),
            'notes',
            'report_file',
            Div(
                Submit('submit', 'Save Result', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
