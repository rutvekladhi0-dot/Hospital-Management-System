from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Department, Specialization


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'branch', 'head', 'phone', 'email', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('branch', css_class='col-md-6'),
            ),
            'description',
            Row(
                Column('head', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name', 'description', 'department', 'is_active']
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
            'is_active',
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )
