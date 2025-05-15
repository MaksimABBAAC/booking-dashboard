from django.core.management.base import BaseCommand
from appointments.utils import generate_appointment_slots
from masters.models import Master
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Генерирует слоты для записи на 2 недели вперед для всех мастеров'

    def handle(self, *args, **options):
        masters = Master.objects.all()
        start_date = date.today()+ timedelta(days=1)
        end_date = start_date + timedelta(days=14)
        
        for master in masters:
            generate_appointment_slots(master, start_date, end_date)
            self.stdout.write(f'Сгенерированы слоты для мастера {master}')
