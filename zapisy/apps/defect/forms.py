from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Defect, DEFECT_MAX_PLACE_SIZE, DEFECT_MAX_NAME_SIZE


class DefectFormBase(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["name", "place", "description", "state"]

    name = forms.CharField(label="Nazwa", max_length=DEFECT_MAX_NAME_SIZE)
    place = forms.CharField(label="Miejsce usterki", max_length=DEFECT_MAX_PLACE_SIZE)

    def __init__(self, *args, **kwargs):
        super(DefectFormBase, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(
            Submit('submit', 'Zapisz', css_class='btn-primary'))


class DefectForm(DefectFormBase):
    def __init__(self, *args, **kwargs):
        super(DefectForm, self).__init__(*args, **kwargs)