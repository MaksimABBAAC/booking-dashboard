from datetime import datetime, timedelta
from schedules.models import DailySchedule
from .models import Appointment

def generate_appointment_slots(master, start_date, end_date):
    """
    Генерация слотов для записи на основе расписания мастера
    между start_date и end_date
    """
    current_date = start_date
    delta = timedelta(days=1)
    
    while current_date <= end_date:
        day_of_week = current_date.weekday()
        
        try:
            daily_schedule = DailySchedule.objects.get(
                weekly_schedule__master=master,
                day_of_week=day_of_week,
                is_working=True
            )
            
            # Генерация слотов на день
            generate_daily_slots(master, current_date, daily_schedule)
            
        except DailySchedule.DoesNotExist:
            # Нет расписания на этот день недели
            pass
        
        current_date += delta

def generate_daily_slots(master, date, daily_schedule):
    start_time = daily_schedule.start_time
    end_time = daily_schedule.end_time
    duration = daily_schedule.appointment_duration
    break_start = daily_schedule.break_start
    break_end = daily_schedule.break_end
    
    current_time = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)
    
    while current_time + timedelta(minutes=duration) <= end_datetime:
        # Проверка на перерыв
        if break_start and break_end:
            break_start_dt = datetime.combine(date, break_start)
            break_end_dt = datetime.combine(date, break_end)
            
            if current_time >= break_start_dt and current_time < break_end_dt:
                current_time = break_end_dt
                continue
        
        # Создание слота
        slot_end = current_time + timedelta(minutes=duration)
        
        Appointment.objects.get_or_create(
            master=master,
            date=date,
            start_time=current_time.time(),
            end_time=slot_end.time(),
            defaults={'is_available': True}
        )
        
        current_time = slot_end