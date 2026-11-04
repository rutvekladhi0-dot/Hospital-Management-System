from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Employee, Attendance, LeaveRequest


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'department', 'designation', 'date_of_joining',
            'salary', 'emergency_contact', 'emergency_phone', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='col-md-6'),
                Column('department', css_class='col-md-6'),
            ),
            Row(
                Column('designation', css_class='col-md-6'),
                Column('date_of_joining', css_class='col-md-6'),
            ),
            Row(
                Column('salary', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            Row(
                Column('emergency_contact', css_class='col-md-6'),
                Column('emergency_phone', css_class='col-md-6'),
            ),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'check_in', 'check_out', 'status', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
            ),
            Row(
                Column('check_in', css_class='col-md-6'),
                Column('check_out', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('remarks', css_class='col-md-6'),
            ),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='col-md-6'),
                Column('leave_type', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            'reason',
            Submit('submit', 'Submit Request', css_class='btn btn-primary'),
        )


class LeaveApprovalForm(forms.Form):
    STATUS_CHOICES = [
        ('Approved', 'Approve'),
        ('Rejected', 'Reject'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
    remarks = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'status',
            'remarks',
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )
