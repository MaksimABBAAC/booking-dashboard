from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['number', 'tg_id']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '79123456789'
            }),
            'tg_id': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789'
            }),
        }
        labels = {
            'number': 'Номер телефона',
            'tg_id': 'Telegram ID (необязательно)'
        }
    def clean_number(self):
        number = self.cleaned_data.get('number')
        if Client.objects.filter(number=number).exists():
            raise forms.ValidationError("Клиент с таким Телефоном уже существует.")  # Ваше собственное сообщение
        return number
        