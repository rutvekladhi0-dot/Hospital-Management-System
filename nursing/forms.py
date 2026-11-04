from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import NursingStation, NursingTask, VitalSigns


class NursingStationForm(forms.ModelForm):
    class Meta:
        model = NursingStation
        fields = ['name', 'ward', 'capacity', 'nurse_in_charge']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('ward', css_class='col-md-6'),
            ),
            Row(
                Column('capacity', css_class='col-md-6'),
                Column('nurse_in_charge', css_class='col-md-6'),
            ),
            Div(
                Submit('submit', 'Save Station', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class NursingTaskForm(forms.ModelForm):
    class Meta:
        model = NursingTask
        fields = ['patient', 'assigned_to', 'task_type', 'description', 'scheduled_time', 'status', 'notes']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6'),
            ),
            Row(
                Column('task_type', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            'scheduled_time',
            'description',
            'notes',
            Div(
                Submit('submit', 'Save Task', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = ['patient', 'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                  'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'weight']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'patient',
            Row(
                Column('temperature', css_class='col-md-4'),
                Column('heart_rate', css_class='col-md-4'),
                Column('weight', css_class='col-md-4'),
            ),
            Row(
                Column('blood_pressure_systolic', css_class='col-md-6'),
                Column('blood_pressure_diastolic', css_class='col-md-6'),
            ),
            Row(
                Column('respiratory_rate', css_class='col-md-6'),
                Column('oxygen_saturation', css_class='col-md-6'),
            ),
            Div(
                Submit('submit', 'Record Vital Signs', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
