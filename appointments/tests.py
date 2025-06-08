from django.core.management import call_command
import json
from django.db import IntegrityError
from django.forms import ValidationError
import pytest
from django.urls import reverse
from rest_framework import status
from schedules.models import DailySchedule, WeeklySchedule
from specialties.models import Specialty
from .models import Appointment
from clients.models import Client
from masters.models import Master
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta, time


class TestAppointment:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpassword")

    @pytest.fixture
    def specialty(self):
        return Specialty.objects.create(name="Тестовая специализация")

    @pytest.fixture
    def master(self, specialty):
        return Master.objects.create(
            name="Иван",
            surname="Иванов",
            patronymic="Иванович",
            description="Описание мастера",
            specialty=specialty,
        )

    @pytest.fixture
    def weekly_schedule(self, master):
        weekly_schedule = WeeklySchedule.objects.create(
            master=master, title="Test Schedule", is_active=True
        )
        DailySchedule.objects.create(
            weekly_schedule=weekly_schedule,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(18, 0),
            break_start=time(12, 0),
            break_end=time(13, 0),
            appointment_duration=30,
            is_working=True,
        )
        return weekly_schedule

    @pytest.fixture
    def client_obj(self):
        return Client.objects.create(number="+79123456789", tg_id=123456789)


@pytest.mark.django_db
class TestAppointmentViews(TestAppointment):

    def test_available_appointments_list_and_generate_slots(
        self, user, client, master, weekly_schedule
    ):
        client.login(username="testuser", password="testpassword")
        call_command("generate_slots")

        response = client.get(
            reverse("appointments:available-appointments"),
        )

        assert response.status_code == 200

        data = json.loads(response.content)
        print("Parsed data:", data)

        assert len(data) > 0, "Список доступных записей пуст"

        found = any(item.get("master") == master.id for item in data)
        assert found, "Мастер не найден в ответе"

    def test_book_appointment(self, user, client, master):
        client.login(username="testuser", password="testpassword")
        slot_date = datetime.now().date() + timedelta(days=1)
        appointment = Appointment.objects.create(
            master=master,
            date=slot_date,
            start_time=datetime.combine(slot_date, time(10, 0)),
            end_time=datetime.combine(slot_date, time(10, 0)) + timedelta(minutes=30),
            is_available=True,
        )
        response = client.post(
            reverse("appointments:book-appointment"),
            {
                "appointment_id": appointment.id,
                "phone_number": "+7 777 7777 777",
                "tg_id": 123,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert Appointment.objects.get(id=appointment.id).is_available is False

    def test_book_appointment_invalid(self, client, user, master):
        client.login(username="testuser", password="testpassword")
        slot_date = datetime.now().date() + timedelta(days=1)
        appointment = Appointment.objects.create(
            master=master,
            date=slot_date,
            start_time=datetime.combine(slot_date, time(10, 0)),
            end_time=datetime.combine(slot_date, time(10, 0)) + timedelta(minutes=30),
            is_available=False,
        )
        response = client.post(
            reverse("appointments:book-appointment"),
            {
                "appointment_id": appointment.id,
                "phone_number": "+7 777 7777 777",
                "tg_id": 123,
            },
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_appointment_update_view(self, client, user, master, client_obj):

        client.login(username="testuser", password="testpassword")
        slot_date = datetime.now().date() + timedelta(days=1)

        appointment = Appointment.objects.create(
            master=master,
            date=slot_date,
            start_time=datetime.combine(slot_date, time(11, 0)),
            end_time=datetime.combine(slot_date, time(11, 0)) + timedelta(minutes=30),
            is_available=False,
            client=client_obj,
        )

        new_appointment = Appointment.objects.create(
            master=master,
            date=slot_date,
            start_time=datetime.combine(slot_date, time(10, 0)),
            end_time=datetime.combine(slot_date, time(10, 0)) + timedelta(minutes=30),
            is_available=True,
        )

        response = client.post(
            reverse("appointments:appointment_edit", args=[appointment.id]),
            {"new_slot": new_appointment.id},
        )

        assert response.status_code == 302
        assert response.url == reverse("clients:client", kwargs={"pk": client_obj.pk})

        new_appointment.refresh_from_db()
        appointment.refresh_from_db()

        assert new_appointment.is_available is False
        assert new_appointment.client == client_obj
        assert appointment.is_available is True
        assert appointment.client is None

        from django.contrib.messages import get_messages

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "Запись успешно перенесена"

    def test_appointment_delete_view(self, client, user, master):
        client.login(username="testuser", password="testpassword")
        slot_date = datetime.now().date() + timedelta(days=1)
        appointment = Appointment.objects.create(
            master=master,
            date=slot_date,
            start_time=datetime.combine(slot_date, time(11, 0)),
            end_time=datetime.combine(slot_date, time(11, 0)) + timedelta(minutes=30),
            is_available=False,
        )
        response = client.post(
            reverse("appointments:appointment_delete", args=[appointment.id])
        )
        assert response.status_code == 302
        assert Appointment.objects.filter(id=appointment.id).count() == 0


@pytest.mark.django_db
class TestAppointmentModel(TestAppointment):

    def test_appointment_creation(self, master):
        appointment = Appointment.objects.create(
            master=master,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        )
        assert (
            appointment.__str__()
            == "2023-01-01 10:00:00-11:00:00 - Иванов Иван Иванович (Свободно)"
        )
        assert Appointment.objects.count() == 1

    def test_appointment_with_client(self, master, client_obj):
        appointment = Appointment.objects.create(
            master=master,
            client=client_obj,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=False,
        )
        assert "Занято" in appointment.__str__()


@pytest.mark.django_db
class TestAppointmentModel(TestAppointment):

    def test_create_available_appointment(self, master):
        appt = Appointment.objects.create(
            master=master,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        )
        assert appt.is_available is True
        assert appt.client is None
        assert "Свободно" in str(appt)

    def test_create_booked_appointment(self, master, client_obj):
        appt = Appointment.objects.create(
            master=master,
            client=client_obj,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=False,
        )
        assert appt.is_available is False
        assert appt.client == client_obj

    def test_clean_valid_available(self, master):
        appt = Appointment(
            master=master,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        )
        appt.full_clean()

    def test_clean_valid_booked(self, master, client_obj):
        appt = Appointment(
            master=master,
            client=client_obj,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=False,
        )
        appt.full_clean()

    def test_clean_invalid_available_with_client(self, master, client_obj):
        appt = Appointment(
            master=master,
            client=client_obj,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        )
        with pytest.raises(ValidationError) as excinfo:
            appt.full_clean()
        assert "Нельзя иметь клиента и быть доступным одновременно" in str(
            excinfo.value
        )

    def test_clean_invalid_booked_without_client(self, master):
        appt = Appointment(
            master=master,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=False,
        )
        with pytest.raises(ValidationError) as excinfo:
            appt.full_clean()
        assert "Нельзя быть занятым без клиента" in str(excinfo.value)

    def test_unique_constraint(self, master):
        Appointment.objects.create(
            master=master,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        )
        with pytest.raises(IntegrityError):
            Appointment.objects.create(
                master=master,
                date=date(2023, 1, 1),
                start_time=time(10, 0),
                end_time=time(11, 30),
                is_available=True,
            )

    def test_time_validation(self, master):
        from django.core.exceptions import ValidationError

        with pytest.raises(ValidationError) as excinfo:
            appt = Appointment(
                master=master,
                date=date(2023, 1, 1),
                start_time=time(11, 0),
                end_time=time(10, 0),
                is_available=True,
            )
            appt.full_clean()

        assert "Время окончания должно быть позже времени начала" in str(excinfo.value)

    def test_master_relation(self, master):
        appt = Appointment.objects.create(
            master=master,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=True,
        )
        assert appt in master.appointments.all()
        assert appt.master == master

    def test_client_relation(self, master, client_obj):
        appt = Appointment.objects.create(
            master=master,
            client=client_obj,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_available=False,
        )
        assert appt in client_obj.appointments.all()
        assert appt.client == client_obj
