from django import forms
from specialties.models import Specialty

class SpecialtyForm(forms.ModelForm):
    
    class Meta:
        model = Specialty
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-input'}),
        }