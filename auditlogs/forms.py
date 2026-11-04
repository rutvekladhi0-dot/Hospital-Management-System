from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import AuditLog

User = get_user_model()


class AuditLogFilterForm(forms.Form):
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
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label='All Users',
        label='User'
    )
    action = forms.ChoiceField(
        choices=[('', 'All Actions')] + AuditLog.ACTION_CHOICES,
        required=False,
        label='Action'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('date_from', css_class='col-md-3'),
                Column('date_to', css_class='col-md-3'),
                Column('user', css_class='col-md-3'),
                Column('action', css_class='col-md-3'),
            ),
            Submit('filter', 'Filter', css_class='btn btn-primary'),
        )
