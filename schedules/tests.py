import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from masters.models import Master
from specialties.models import Specialty
from .forms import WeeklyScheduleCreateForm, DailyScheduleForm
from datetime import time
from .models import WeeklySchedule, DailySchedule


class TestSchedule:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpassword')
    
    @pytest.fixture
    def specialty(self):
        return Specialty.objects.create(name='Тестовая специализация')

    @pytest.fixture
    def master(self, specialty):
        return Master.objects.create(
            name='Иван',
            surname='Иванов',
            patronymic='Иванович',
            description='Описание мастера',
            specialty=specialty
        )

    @pytest.fixture
    def weekly_schedule(self, master):
        return WeeklySchedule.objects.create(master=master, title='Test Schedule')



@pytest.mark.django_db
class TestWeeklyScheduleViews(TestSchedule):

    
    def test_weekly_schedule_list_view(self, user, client):
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('schedules:schedules'))
        assert response.status_code == 200
        assert 'schedules/weekly_schedule_list.html' in [t.name for t in response.templates]

    def test_weekly_schedule_create_view(self, user, client, master):
        client.login(username='testuser', password='testpassword')
        url = reverse('schedules:schedule_add')
        response = client.post(url, {
            'master': master.id,
            'title': 'New Schedule',
            'is_active': True,
        })
        assert response.status_code == 302
        assert WeeklySchedule.objects.filter(title='New Schedule').exists()

    def test_weekly_schedule_update_view(self, user, client, weekly_schedule):
        client.login(username='testuser', password='testpassword')
        url = reverse('schedules:schedule_edit', kwargs={'pk': weekly_schedule.pk})
        response = client.post(url, {
            'master': weekly_schedule.master.id,
            'title': 'Updated Schedule',
            'is_active': True,
        })
        assert response.status_code == 302
        weekly_schedule.refresh_from_db()
        assert weekly_schedule.title == 'Updated Schedule'

    def test_delete_schedule(self, user, client, weekly_schedule):
        client.login(username='testuser', password='testpassword')

        assert WeeklySchedule.objects.filter(pk=weekly_schedule.pk).exists()

        url = reverse('schedules:schedule_delete', kwargs={'pk': weekly_schedule.pk})
        response = client.post(url)

        assert not WeeklySchedule.objects.filter(pk=weekly_schedule.pk).exists()
        assert response.status_code == 302
        assert response.url == reverse('schedules:schedules')


@pytest.mark.django_db
class TestDailyScheduleForm:

    def test_valid_data(self):
        form_data = {
            'is_working': True,
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'appointment_duration': 30,
            'break_start': time(12, 0),
            'break_end': time(13, 0),
        }
        form = DailyScheduleForm(data=form_data)
        assert form.is_valid()

    def test_invalid_end_time_before_start(self):
        form_data = {
            'is_working': True,
            'start_time': time(9, 0),
            'end_time': time(8, 0),
            'appointment_duration': 30,
            'break_start': time(12, 0),
            'break_end': time(13, 0),
        }
        form = DailyScheduleForm(data=form_data)
        assert not form.is_valid()
        assert 'end_time' in form.errors

    def test_invalid_break_times(self):
        form_data = {
            'is_working': True,
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'appointment_duration': 30,
            'break_start': time(14, 0),
            'break_end': time(13, 0),
        }
        form = DailyScheduleForm(data=form_data)
        assert not form.is_valid()
        assert 'break_end' in form.errors

    def test_appointment_duration_longer_than_workday(self):
        form_data = {
            'is_working': True,
            'start_time': time(9, 0),
            'end_time': time(10, 0),
            'appointment_duration': 120,
            'break_start': time(9, 30),
            'break_end': time(9, 45),
        }
        form = DailyScheduleForm(data=form_data)
        assert not form.is_valid()
        assert 'appointment_duration' in form.errors


@pytest.mark.django_db
class TestWeeklyScheduleCreateForm(TestSchedule):

    def test_valid_data(self, user, master):
        form_data = {
            'master': master.id,
            'title': 'Valid Schedule',
            'is_active': True,
        }
        form = WeeklyScheduleCreateForm(data=form_data)
        assert form.is_valid()

    def test_missing_master(self):
        form_data = {
            'master': '',
            'title': 'Schedule without Master',
            'is_active': True,
        }
        form = WeeklyScheduleCreateForm(data=form_data)
        assert not form.is_valid()
        assert 'master' in form.errors

    def test_missing_title(self, user):
        form_data = {
            'master': user.id,
            'title': '',
            'is_active': True,
        }
        form = WeeklyScheduleCreateForm(data=form_data)
        assert not form.is_valid()
        assert 'title' in form.errors

    def test_empty_form(self):
        form = WeeklyScheduleCreateForm(data={})
        assert not form.is_valid()
        assert 'master' in form.errors
        assert 'title' in form.errors


@pytest.mark.django_db
class TestWeeklyScheduleModel(TestSchedule):

    def test_create_weekly_schedule(self, user, master):
        schedule = WeeklySchedule.objects.create(master=master, title='Test Schedule', is_active=True)
        assert schedule.pk is not None
        assert schedule.master == master
        assert schedule.title == 'Test Schedule'
        assert schedule.is_active is True

    def test_update_weekly_schedule(self, user, master):
        schedule = WeeklySchedule.objects.create(master=master, title='Old Title', is_active=False)
        schedule.title = 'New Title'
        schedule.is_active = True
        schedule.save()
        updated = WeeklySchedule.objects.get(pk=schedule.pk)
        assert updated.title == 'New Title'
        assert updated.is_active is True

    def test_delete_weekly_schedule(self, user, master):
        schedule = WeeklySchedule.objects.create(master=master, title='To Delete', is_active=True)
        pk = schedule.pk
        schedule.delete()
        with pytest.raises(WeeklySchedule.DoesNotExist):
            WeeklySchedule.objects.get(pk=pk)


@pytest.mark.django_db
class TestDailyScheduleModel(TestSchedule):

    def test_create_daily_schedule(self, user, master):
        weekly = WeeklySchedule.objects.create(master=master, title='Weekly', is_active=True)
        daily = DailySchedule.objects.create(
            weekly_schedule=weekly,
            is_working=True,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
            appointment_duration=30,
            break_start=time(12, 0),
            break_end=time(13, 0),
        )
        assert daily.pk is not None
        assert daily.weekly_schedule == weekly
        assert daily.is_working is True
        assert daily.start_time == time(9, 0)
        assert daily.end_time == time(17, 0)
        assert daily.appointment_duration == 30
        assert daily.break_start == time(12, 0)
        assert daily.break_end == time(13, 0)

    def test_update_daily_schedule(self, user, master):
        weekly = WeeklySchedule.objects.create(master=master, title='Weekly2', is_active=True)
        daily = DailySchedule.objects.create(
            weekly_schedule=weekly,
            is_working=True,
            day_of_week=0,
            start_time=time(8, 0),
            end_time=time(16, 0),
            appointment_duration=20,
            break_start=time(11, 0),
            break_end=time(11, 30),
        )
        daily.appointment_duration = 25
        daily.end_time = time(17, 0)
        daily.save()
        updated = DailySchedule.objects.get(pk=daily.pk)
        assert updated.appointment_duration == 25
        assert updated.end_time == time(17, 0)

    def test_delete_daily_schedule(self, user, master):
        weekly = WeeklySchedule.objects.create(master=master, title='Weekly3', is_active=True)
        daily = DailySchedule.objects.create(
            weekly_schedule=weekly,
            is_working=False,
            day_of_week=0,
        )
        pk = daily.pk
        daily.delete()
        with pytest.raises(DailySchedule.DoesNotExist):
            DailySchedule.objects.get(pk=pk)
