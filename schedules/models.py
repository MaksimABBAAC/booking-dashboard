from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from masters.models import Master

class WeeklySchedule(models.Model):
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name='Мастер',
        related_name='weekly_schedules'
    )
    title = models.CharField(
        max_length=100,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = 'Недельное расписание'
        verbose_name_plural = 'Недельные расписания'
        ordering = ['master', 'title']

    def __str__(self):
        return f'{self.master} — {self.title or "Расписание"}'

class DailySchedule(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )

    weekly_schedule = models.ForeignKey(
        WeeklySchedule,
        on_delete=models.CASCADE,
        related_name='days'
    )
    day_of_week = models.IntegerField(
        'День недели',
        choices=DAYS_OF_WEEK
    )
    is_working = models.BooleanField(
        'Рабочий день',
        default=True
    )
    start_time = models.TimeField(
        'Начало работы',
        default='09:00',
        blank=True,
        null=True
    )
    end_time = models.TimeField(
        'Окончание работы',
        default='18:00',
        blank=True,
        null=True
    )
    appointment_duration = models.PositiveIntegerField(
        'Длительность приёма (мин)',
        default=30,
        validators=[MinValueValidator(5), MaxValueValidator(240)]
    )
    break_start = models.TimeField(
        'Начало перерыва',
        blank=True,
        null=True
    )
    break_end = models.TimeField(
        'Конец перерыва',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Дневное расписание'
        verbose_name_plural = 'Дневные расписания'
        unique_together = [['weekly_schedule', 'day_of_week']]
        ordering = ['day_of_week']

    def __str__(self):
        return f'{self.get_day_of_week_display()} ({self.weekly_schedule})'
    
