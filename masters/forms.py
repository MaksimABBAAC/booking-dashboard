
from django import forms
from masters.models import Masters


class AddMasterForm(forms.ModelForm):
    
    class Meta:
        model = Masters
        fields = ['name', 'surname', 'patronymic', 'description']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-input'}),
            'surname' : forms.TextInput(attrs={'class': 'form-input'}),
            'patronymic' : forms.TextInput(attrs={'class': 'form-input'}),
            'description' : forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }