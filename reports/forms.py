from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ReportFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date From'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date To'
    )
    department = forms.CharField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Department'
    )

    def __init__(self, *args, **kwargs):
        department_choices = kwargs.pop('department_choices', None)
        super().__init__(*args, **kwargs)
        if department_choices is not None:
            self.fields['department'].widget = forms.Select(
                choices=[('', 'All Departments')] + [(d['name'], d['name']) for d in department_choices],
                attrs={'class': 'form-select'}
            )
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('date_from', css_class='col-md-3'),
                Column('date_to', css_class='col-md-3'),
                Column('department', css_class='col-md-3'),
                Column(Submit('filter', 'Filter', css_class='btn btn-primary'), css_class='col-md-3 d-flex align-items-end'),
            ),
        )
