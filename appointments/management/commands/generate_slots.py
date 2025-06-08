from datetime import date, timedelta

from django.core.management.base import BaseCommand

from appointments.models import Appointment
from appointments.utils import generate_appointment_slots
from masters.models import Master


class Command(BaseCommand):
    help = "Генерирует слоты для записи на 2 недели вперед для всех мастеров"

    def handle(self, *args, **options):
        masters = Master.objects.all()
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=14)

        for master in masters:
            generate_appointment_slots(master, start_date, end_date)
            self.stdout.write(f"Сгенерированы слоты для мастера {master}")

        appointment_count = Appointment.objects.count()
        self.stdout.write(f"Всего создано записей: {appointment_count}")
