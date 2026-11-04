from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import RadiologyTest, RadiologyOrder, RadiologyReport
from doctors.models import Doctor

User = get_user_model()


class RadiologyTestForm(forms.ModelForm):
    class Meta:
        model = RadiologyTest
        fields = ['name', 'description', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('price', css_class='col-md-6'),
            ),
            'description',
            'is_active',
            Div(
                Submit('submit', 'Save Test', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class RadiologyOrderForm(forms.ModelForm):
    class Meta:
        model = RadiologyOrder
        fields = ['patient', 'doctor', 'test', 'appointment', 'clinical_information', 'priority']
        widgets = {
            'clinical_information': forms.Textarea(attrs={'rows': 4}),
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'test': forms.Select(attrs={'class': 'form-select'}),
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        doctor_users = Doctor.objects.select_related('employee__user', 'specialization').all()
        self.fields['doctor'].queryset = User.objects.filter(
            id__in=doctor_users.values_list('employee__user_id', flat=True)
        )
        self.fields['doctor'].label_from_instance = lambda user: user.get_full_name() or user.username
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('doctor', css_class='col-md-6'),
            ),
            Row(
                Column('test', css_class='col-md-6'),
                Column('appointment', css_class='col-md-6'),
            ),
            Row(
                Column('priority', css_class='col-md-6'),
            ),
            'clinical_information',
            Div(
                Submit('submit', 'Create Order', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class RadiologyReportForm(forms.ModelForm):
    class Meta:
        model = RadiologyReport
        fields = ['findings', 'impression', 'image_file', 'report_file']
        widgets = {
            'findings': forms.Textarea(attrs={'rows': 5}),
            'impression': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'findings',
            'impression',
            Row(
                Column('image_file', css_class='col-md-6'),
                Column('report_file', css_class='col-md-6'),
            ),
            Div(
                Submit('submit', 'Save Report', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
