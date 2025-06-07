from datetime import datetime
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from clients.models import Client
from masters.models import Master

class Appointment(models.Model):
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name='Мастер',
        related_name='appointments'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        verbose_name='Клиент',
        null=True,
        blank=True,
        related_name='appointments'
    )
    date = models.DateField('Дата приема')
    start_time = models.TimeField('Время начала')
    end_time = models.TimeField('Время окончания')
    is_available = models.BooleanField('Доступен для записи', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['date', 'start_time']
        unique_together = ['master', 'date', 'start_time']

    def __str__(self):
        status = "Свободно" if self.is_available else f"Занято ({self.client})"
        return f"{self.date} {self.start_time}-{self.end_time} - {self.master} ({status})"
    
    def clean(self):
        if self.start_time and self.end_time:
            start_datetime = timezone.make_aware(
                datetime.combine(self.date, self.start_time)
            )
            end_datetime = timezone.make_aware(
                datetime.combine(self.date, self.end_time)
            )
            
            if end_datetime <= start_datetime:
                raise ValidationError(
                    "Время окончания должно быть позже времени начала"
                )
        
        if self.client and self.is_available:
            raise ValidationError("Нельзя иметь клиента и быть доступным одновременно")
        if not self.client and not self.is_available:
            raise ValidationError("Нельзя быть занятым без клиента")
