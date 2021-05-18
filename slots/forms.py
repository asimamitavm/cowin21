from django import forms
from .models import slotrequest,State,District

class DateInput(forms.DateInput):
    input_type = 'date'

class RequestByPinForm(forms.ModelForm):
    class Meta:
        model = slotrequest
        fields = ('date','pin','email')
        widgets = {'date': DateInput(),}

class RequestByDistForm(forms.ModelForm):
    class Meta:
        model = slotrequest
        fields = ('state','district','date','email')
        widgets = {'date': DateInput(),}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'state' in self.data:
            try:
                stid = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=stid).all()
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryse
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.state.district_set.all()
