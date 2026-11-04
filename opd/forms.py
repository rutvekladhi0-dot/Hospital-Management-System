from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import OPDVisit


class OPDVisitForm(forms.ModelForm):
    class Meta:
        model = OPDVisit
        fields = ['patient', 'doctor', 'appointment', 'visit_date', 'symptoms',
                  'diagnosis', 'treatment', 'doctor_notes', 'follow_up_date', 'status']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'doctor_notes': forms.Textarea(attrs={'rows': 3}),
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
                Column('appointment', css_class='col-md-6'),
                Column('visit_date', css_class='col-md-6'),
            ),
            'symptoms',
            'diagnosis',
            'treatment',
            'doctor_notes',
            Row(
                Column('follow_up_date', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            Div(
                Submit('submit', 'Save Visit', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
