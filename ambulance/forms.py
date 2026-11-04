from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Ambulance, AmbulanceRequest


class AmbulanceForm(forms.ModelForm):
    class Meta:
        model = Ambulance
        fields = ['vehicle_number', 'vehicle_type', 'is_available', 'driver_name',
                  'driver_phone', 'current_location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('vehicle_number', css_class='col-md-6'),
                Column('vehicle_type', css_class='col-md-6'),
            ),
            Row(
                Column('driver_name', css_class='col-md-6'),
                Column('driver_phone', css_class='col-md-6'),
            ),
            'current_location',
            'is_available',
            Div(
                Submit('submit', 'Save Ambulance', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class AmbulanceRequestForm(forms.ModelForm):
    class Meta:
        model = AmbulanceRequest
        fields = ['patient_name', 'patient_phone', 'pickup_location', 'dropoff_location',
                  'ambulance', 'status', 'distance_km']
        widgets = {
            'pickup_location': forms.Textarea(attrs={'rows': 2}),
            'dropoff_location': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ambulance'].queryset = Ambulance.objects.filter(is_available=True)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient_name', css_class='col-md-6'),
                Column('patient_phone', css_class='col-md-6'),
            ),
            'pickup_location',
            'dropoff_location',
            Row(
                Column('ambulance', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            'distance_km',
            Div(
                Submit('submit', 'Save Request', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )
