from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    phone_number = forms.CharField(required=True)
    tg_id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "123456789"}
        ),
    )
    appointment_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_tg_id(self):
        tg_id = self.cleaned_data.get("tg_id")
        return tg_id if tg_id else None

    def clean_number(self):
        number = self.cleaned_data.get("number")
        if Client.objects.filter(number=number).exists():
            raise forms.ValidationError("Клиент с таким Телефоном уже существует.")
        return number
