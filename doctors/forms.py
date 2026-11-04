from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Doctor, DoctorSchedule, DoctorAvailability


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'employee', 'specialization', 'consultation_fee',
            'bio', 'years_of_experience', 'is_available'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='col-md-6'),
                Column('specialization', css_class='col-md-6'),
            ),
            Row(
                Column('consultation_fee', css_class='col-md-4'),
                Column('years_of_experience', css_class='col-md-4'),
                Column('is_available', css_class='col-md-4'),
            ),
            'bio',
            Submit('submit', 'Save Doctor', css_class='btn btn-primary'),
        )


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'day_of_week', 'start_time', 'end_time', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('doctor', css_class='col-md-6'),
                Column('day_of_week', css_class='col-md-6'),
            ),
            Row(
                Column('start_time', css_class='col-md-5'),
                Column('end_time', css_class='col-md-5'),
                Column('is_active', css_class='col-md-2'),
            ),
            Submit('submit', 'Save Schedule', css_class='btn btn-primary'),
        )


class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'date', 'start_time', 'end_time', 'is_available', 'max_patients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('doctor', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
            ),
            Row(
                Column('start_time', css_class='col-md-4'),
                Column('end_time', css_class='col-md-4'),
                Column('max_patients', css_class='col-md-4'),
            ),
            'is_available',
            Submit('submit', 'Save Availability', css_class='btn btn-primary'),
        )
