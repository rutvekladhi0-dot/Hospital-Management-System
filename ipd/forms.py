from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Ward, Bed, Admission, BedTransfer


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['name', 'department', 'floor', 'capacity', 'ward_type', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('department', css_class='col-md-6'),
            ),
            Row(
                Column('floor', css_class='col-md-4'),
                Column('capacity', css_class='col-md-4'),
                Column('ward_type', css_class='col-md-4'),
            ),
            'is_active',
            Div(
                Submit('submit', 'Save Ward', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['ward', 'bed_number', 'bed_type', 'status', 'daily_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('ward', css_class='col-md-6'),
                Column('bed_number', css_class='col-md-6'),
            ),
            Row(
                Column('bed_type', css_class='col-md-4'),
                Column('status', css_class='col-md-4'),
                Column('daily_rate', css_class='col-md-4'),
            ),
            Div(
                Submit('submit', 'Save Bed', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'doctor', 'admission_type', 'ward', 'bed', 'diagnosis']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bed'].queryset = Bed.objects.filter(status='Available')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('doctor', css_class='col-md-6'),
            ),
            Row(
                Column('admission_type', css_class='col-md-4'),
                Column('ward', css_class='col-md-4'),
                Column('bed', css_class='col-md-4'),
            ),
            'diagnosis',
            Div(
                Submit('submit', 'Admit Patient', css_class='btn btn-primary'),
                css_class='mt-3'
            )
        )


class DischargeForm(forms.Form):
    discharge_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'discharge_notes',
            Div(
                Submit('submit', 'Discharge Patient', css_class='btn btn-warning'),
                css_class='mt-3'
            )
        )


class BedTransferForm(forms.ModelForm):
    class Meta:
        model = BedTransfer
        fields = ['to_ward', 'to_bed', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_bed'].queryset = Bed.objects.filter(status='Available')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('to_ward', css_class='col-md-6'),
                Column('to_bed', css_class='col-md-6'),
            ),
            'reason',
            Div(
                Submit('submit', 'Transfer Bed', css_class='btn btn-info'),
                css_class='mt-3'
            )
        )
