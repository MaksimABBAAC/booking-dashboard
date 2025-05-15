from celery.schedules import crontab
from app import app

app.conf.beat_schedule = {
    'generate-slots-every-day': {
        'task': 'appointments.tasks.generate_daily_slots',
        'schedule': crontab(hour=3, minute=0),
    },
}
