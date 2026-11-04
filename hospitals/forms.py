from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'phone', 'is_main_branch', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            'address',
            Row(
                Column('is_main_branch', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )
