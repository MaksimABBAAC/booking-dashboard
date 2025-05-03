from datetime import time
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from specialties.models import Specialty

class Master(models.Model):

    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150)
    description = models.TextField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "master"
        verbose_name_plural = "masters"
        db_table = 'masters'


class Schedule(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )

    master = models.ForeignKey(
        'Master',
        on_delete=models.CASCADE,
    )
    
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
    )
    
    is_working = models.BooleanField(
        default=True,
    )
    
    start_time = models.TimeField(
        default=time(9, 0),
        null=True,
        blank=True
    )
    
    end_time = models.TimeField(
        default=time(18, 0),
        null=True,
        blank=True
    )
    
    appointment_duration = models.PositiveIntegerField(
        verbose_name='Длительность приема (минуты)',
        default=30,
        validators=[MinValueValidator(5), MaxValueValidator(240)]
    )
    
    break_start = models.TimeField(
        null=True,
        blank=True
    )
    
    break_end = models.TimeField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'schedule'
        verbose_name_plural = 'schedules'
        db_table = 'schedule'
        
