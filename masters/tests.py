import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from specialties.models import Specialty
from .models import Master
from .forms import MasterForm
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestMasterViews:

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

    def test_master_list_view(self, client):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        url = reverse("masters:masters")
        response = client.get(url)
        assert response.status_code == 200
        assert "masters" in response.context

    def test_master_detail_view(self, client, master):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        url = reverse("masters:master", args=[master.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["master"] == master

    def test_master_create_view(self, client):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        specialty = Specialty.objects.create(name="Тестовая специальность")
        url = reverse("masters:master_add")
        data = {
            "name": "Петр",
            "surname": "Петров",
            "patronymic": "Петрович",
            "description": "Описание нового мастера",
            "specialty": specialty.pk,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Master.objects.filter(name="Петр").exists()

    def test_master_update_view(self, client, master):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        specialty = Specialty.objects.create(name="Тестовая специальность")
        url = reverse("masters:master_edit", args=[master.pk])
        data = {
            "name": "Иван обновленный",
            "surname": "Иванов",
            "patronymic": "Иванович",
            "description": "Обновленное описание",
            "specialty": specialty.pk,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        master.refresh_from_db()
        assert master.name == "Иван обновленный"

    def test_master_delete_view(self, client, master):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        url = reverse("masters:master_delete", args=[master.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert not Master.objects.filter(pk=master.pk).exists()


@pytest.mark.django_db
class TestMasterAPI:

    @pytest.fixture
    def api_client(self):
        return APIClient()

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

    def test_api_master_list(self, api_client):
        url = reverse("masters:api_masters")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)


class TestMasterForm:
    @pytest.mark.django_db
    def test_master_form_valid_data(specialty):
        specialty = Specialty.objects.create(name="Тестовая специальность")
        form_data = {
            "name": "Иван",
            "surname": "Иванов",
            "patronymic": "Иванович",
            "description": "Описание мастера",
            "specialty": specialty.pk,
        }
        form = MasterForm(data=form_data)
        assert form.is_valid()
