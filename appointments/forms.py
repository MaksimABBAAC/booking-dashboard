from datetime import timedelta
from django import forms
from django.utils import timezone
from .models import Appointment

class BookingForm(forms.Form):
    appointment_id = forms.IntegerField(widget=forms.HiddenInput())
    phone_number = forms.CharField(
        label='Номер телефона',
        max_length=20,
        required=True
    )
    tg_id = forms.CharField(
        label='Telegram ID (необязательно)',
        max_length=100,
        required=False
    )

class AppointmentRescheduleForm(forms.ModelForm):
    new_slot = forms.ModelChoiceField(
        queryset=Appointment.objects.none(),
        label="Выберите новый слот",
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    class Meta:
        model = Appointment
        fields = []
    
    def __init__(self, *args, **kwargs):
        current_master = kwargs.pop('current_master', None)
        super().__init__(*args, **kwargs)
        
        if current_master:
            self.fields['new_slot'].queryset = Appointment.objects.filter(
                master=current_master,
                is_available=True,
                date__gte=timezone.now() + timedelta(days=1)
            ).exclude(pk=self.instance.pk).order_by('date', 'start_time')
