import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from clients.forms import ClientForm
from .models import Client


@pytest.mark.django_db
class TestClientViews:

    @pytest.fixture
    def client_obj(self):
        return Client.objects.create(number='+79123456789', tg_id=123456789)

    def test_client_list_view(self, client, client_obj):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        url = reverse('clients:clients')
        response = client.get(url)
        assert response.status_code == 200
        assert client_obj in response.context['clients']

    def test_client_detail_view(self, client, client_obj):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        url = reverse('clients:client', args=[client_obj.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['client'] == client_obj

    def test_client_create_view(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        url = reverse('clients:client_add')
        data = {
            'number': '+79123456789',
            'tg_id': 123456789
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Client.objects.filter(number='+79123456789').exists()

    def test_client_update_view(self, client, client_obj):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        url = reverse('clients:client_edit', args=[client_obj.pk])
        data = {
            'number': '+79234567890',
            'tg_id': 987654321
        }
        response = client.post(url, data)
        assert response.status_code == 302
        client_obj.refresh_from_db()
        assert client_obj.number == '+79234567890'
        assert client_obj.tg_id == 987654321

    def test_client_delete_view(self, client, client_obj):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        url = reverse('clients:client_delete', args=[client_obj.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert not Client.objects.filter(pk=client_obj.pk).exists()

    def test_client_search_view(self, client, client_obj):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        url = reverse('clients:clients') + '?phone_search=79123456789'
        response = client.get(url)
        assert response.status_code == 200
        assert client_obj in response.context['clients']

@pytest.mark.django_db
class TestClientModel:

    def test_client_creation(self):
        client = Client.objects.create(number='+79123456789', tg_id=123456789)
        assert client.number == '+79123456789'
        assert client.tg_id == 123456789
        assert str(client) == '+79123456789'

    def test_unique_phone_number(self):
        Client.objects.create(number='+79123456789', tg_id=123456789)
        with pytest.raises(Exception):
            Client.objects.create(number='+79123456789', tg_id=987654321)


@pytest.mark.django_db
class TestClientForm:
    @pytest.fixture
    def client_obj(self):
        return Client.objects.create(number='+79123456789', tg_id=123456789)

    def test_valid_form(self):
        form_data = {
            'number': '+79123456789',
            'tg_id': 123456789
        }
        form = ClientForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data['number'] == '+79123456789'
        assert form.cleaned_data['tg_id'] == 123456789

    def test_invalid_form_without_number(self):
        form_data = {
            'number': '',
            'tg_id': 123456789
        }
        form = ClientForm(data=form_data)
        assert not form.is_valid()
        assert 'number' in form.errors

    def test_invalid_form_with_duplicate_number(self, client_obj):
        form_data = {
            'number': client_obj.number,
            'tg_id': 987654321
        }
        form = ClientForm(data=form_data)
        assert not form.is_valid()
        assert 'number' in form.errors
        assert form.errors['number'] == ['Клиент с таким Телефоном уже существует.']
