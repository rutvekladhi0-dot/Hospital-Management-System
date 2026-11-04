from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Appointment, Visit


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient', 'doctor', 'appointment_date', 'appointment_time',
            'department', 'appointment_type', 'reason', 'notes'
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
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
            Row(
                Column('appointment_date', css_class='col-md-4'),
                Column('appointment_time', css_class='col-md-4'),
                Column('appointment_type', css_class='col-md-4'),
            ),
            'department',
            'reason',
            'notes',
            Submit('submit', 'Book Appointment', css_class='btn btn-primary'),
        )


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'status',
            'notes',
            Submit('submit', 'Update Appointment', css_class='btn btn-primary'),
        )


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['appointment', 'doctor_notes', 'diagnosis', 'follow_up_date']
        widgets = {
            'doctor_notes': forms.Textarea(attrs={'rows': 4}),
            'diagnosis': forms.Textarea(attrs={'rows': 4}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'appointment',
            'diagnosis',
            'doctor_notes',
            'follow_up_date',
            Submit('submit', 'Save Visit', css_class='btn btn-primary'),
        )
