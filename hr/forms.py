from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Designation, HRRecord, Training


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'department', 'description']
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
            Div(
                Submit('submit', 'Save Designation', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class HRRecordForm(forms.ModelForm):
    class Meta:
        model = HRRecord
        fields = ['employee', 'record_type', 'effective_date', 'description']
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='col-md-6'),
                Column('record_type', css_class='col-md-6'),
            ),
            'effective_date',
            'description',
            Div(
                Submit('submit', 'Save HR Record', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['title', 'description', 'trainer', 'start_date', 'end_date', 'employees', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'employees': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-8'),
                Column('status', css_class='col-md-4'),
            ),
            'trainer',
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            'description',
            'employees',
            Div(
                Submit('submit', 'Save Training', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
