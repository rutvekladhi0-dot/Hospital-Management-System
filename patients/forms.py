from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Patient, MedicalRecord, PatientDocument


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'user', 'blood_group', 'allergies', 'medical_history',
            'emergency_contact_name', 'emergency_contact_phone', 'insurance_provider'
        ]
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='col-md-6'),
                Column('blood_group', css_class='col-md-6'),
            ),
            Row(
                Column('emergency_contact_name', css_class='col-md-6'),
                Column('emergency_contact_phone', css_class='col-md-6'),
            ),
            'insurance_provider',
            HTML('<hr><h5>Medical Information</h5>'),
            'allergies',
            'medical_history',
            Submit('submit', 'Save Patient', css_class='btn btn-primary'),
        )


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'visit_date', 'diagnosis', 'symptoms', 'notes']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('doctor', css_class='col-md-6'),
            ),
            'visit_date',
            'diagnosis',
            'symptoms',
            'notes',
            Submit('submit', 'Save Record', css_class='btn btn-primary'),
        )


class PatientDocumentForm(forms.ModelForm):
    class Meta:
        model = PatientDocument
        fields = ['document_type', 'title', 'description', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (optional)'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
