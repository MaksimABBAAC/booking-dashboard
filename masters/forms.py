
from django import forms
from masters.models import Master, Schedule
from django.core.exceptions import ValidationError
from specialties.models import Specialty

# class ScheduleForm(forms.ModelForm):
#     class Meta:
#         model = Schedule
#         fields = '__all__'
#         widgets = {
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time'}),
#             'break_start': forms.TimeInput(attrs={'type': 'time'}),
#             'break_end': forms.TimeInput(attrs={'type': 'time'}),
#             'appointment_duration': forms.NumberInput(attrs={'min': 5, 'max': 240}),
#         }
#         labels = {
#             'day_of_week': 'День недели',
#             'is_working': 'Рабочий день',
#             'start_time': 'Начало работы',
#             'end_time': 'Окончание работы',
#             'appointment_duration': 'Длительность приема (минут)',
#             'break_start': 'Начало перерыва',
#             'break_end': 'Окончание перерыва',
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         is_working = cleaned_data.get('is_working')
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')
#         break_start = cleaned_data.get('break_start')
#         break_end = cleaned_data.get('break_end')
#         duration = cleaned_data.get('appointment_duration')

#         if is_working:
#             # Проверка рабочего времени
#             if not start_time or not end_time:
#                 raise ValidationError("Для рабочего дня укажите время начала и окончания работы")
            
#             if start_time >= end_time:
#                 raise ValidationError("Время начала должно быть раньше времени окончания")

#             # Проверка перерыва
#             if break_start or break_end:
#                 if not (break_start and break_end):
#                     raise ValidationError("Укажите начало и окончание перерыва")
                
#                 if break_start >= break_end:
#                     raise ValidationError("Время начала перерыва должно быть раньше окончания")
                
#                 if break_start < start_time or break_end > end_time:
#                     raise ValidationError("Перерыв должен быть в пределах рабочего времени")

#             # Проверка что длительность приема помещается в рабочее время
#             if duration and start_time and end_time:
#                 total_minutes = (end_time.hour - start_time.hour) * 60 + (end_time.minute - start_time.minute)
#                 if duration > total_minutes:
#                     raise ValidationError("Длительность приема не может быть больше рабочего времени")

#         return cleaned_data

class MasterForm(forms.ModelForm):

    class Meta:

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['specialty'].queryset = Specialty.objects.all()
            self.fields['specialty'].empty_label = "Выберите специализацию"
            self.fields['specialty'].label = "Специализация"

        model = Master
        fields = ['name', 'surname', 'patronymic', 'description', 'specialty']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-input'}),
            'surname' : forms.TextInput(attrs={'class': 'form-input'}),
            'patronymic' : forms.TextInput(attrs={'class': 'form-input'}),
            'description' : forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'specialty': forms.Select(attrs={'class': 'form-select'}),
        }
            
