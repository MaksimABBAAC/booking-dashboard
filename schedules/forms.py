from .models import WeeklySchedule, DailySchedule
from django import forms
from django.core.exceptions import ValidationError


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

class DailyScheduleForm(forms.ModelForm):
    class Meta:
        model = DailySchedule
        fields = ['is_working', 'start_time', 'end_time', 'appointment_duration', 'break_start', 'break_end']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'appointment_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_working': forms.CheckboxInput(attrs={'class': 'form-check-input', 'onchange': 'toggleDayFields(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля необязательными, если день не рабочий
        if not self.instance or not self.instance.is_working:
            for field in ['start_time', 'end_time', 'appointment_duration', 'break_start', 'break_end']:
                self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_working = cleaned_data.get('is_working')
        if not is_working:
            return cleaned_data  # Пропускаем проверки для нерабочих дней

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        break_start = cleaned_data.get('break_start')
        break_end = cleaned_data.get('break_end')
        duration = cleaned_data.get('appointment_duration')

        errors = {}

        # Проверка рабочего времени
        if not start_time:
            errors['start_time'] = "Укажите время начала работы"
        if not end_time:
            errors['end_time'] = "Укажите время окончания работы"
        
        if start_time and end_time and start_time >= end_time:
            errors['end_time'] = "Время окончания должно быть позже времени начала"

        # Проверка перерыва
        if break_start or break_end:
            if not break_start:
                errors['break_start'] = "Укажите начало перерыва"
            if not break_end:
                errors['break_end'] = "Укажите окончание перерыва"
            
            if break_start and break_end:
                if break_start >= break_end:
                    errors['break_end'] = "Окончание перерыва должно быть позже его начала"
                if start_time and break_start < start_time:
                    errors['break_start'] = "Перерыв не может начинаться до начала рабочего дня"
                if end_time and break_end > end_time:
                    errors['break_end'] = "Перерыв не может заканчиваться после окончания рабочего дня"

        # Проверка длительности приема
        if duration and start_time and end_time:
            total_minutes = (end_time.hour - start_time.hour) * 60 + (end_time.minute - start_time.minute)
            if duration > total_minutes:
                errors['appointment_duration'] = (
                    f"Длительность приема ({duration} мин) превышает рабочий день "
                    f"({total_minutes} мин между {start_time.strftime('%H:%M')} и {end_time.strftime('%H:%M')})"
                )

        if errors:
            raise ValidationError(errors)

        return cleaned_data
class WeeklyScheduleCreateForm(forms.ModelForm):
    class Meta:
        model = WeeklySchedule
        fields = ['master', 'title', 'is_active']
        widgets = {
            'master': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daily_forms = []
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            form = DailyScheduleForm(prefix=prefix)
            self.daily_forms.append((day_name, form))