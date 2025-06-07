import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from specialties.models import Specialty
from specialties.forms import SpecialtyForm


class Test_specialty_model():
    
    @pytest.mark.django_db
    def test_specialty_str_method(self):
        specialty = Specialty(name='test')
        assert str(specialty) == 'test'

class Test_specialty_form():
    def test_specialty_form_valid_data(self):
        form_data = {'name': 'test'}
        form = SpecialtyForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data['name'] == 'test'

    def test_specialty_form_invalid_data(self):
        form_data = {'name': ''}
        form = SpecialtyForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors

class Test_specialty_views():

    @pytest.mark.django_db
    def test_specialty_list_view(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        Specialty.objects.create(name='test')
        response = client.get(reverse('specialties:specialties'))
        assert response.status_code == 200
        assert 'specialties' in response.context
        assert len(response.context['specialties']) == 1
    
    @pytest.mark.django_db
    def test_specialty_create_view(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        response = client.post(reverse('specialties:specialty_add'), {'name': 'test'})
        assert response.status_code == 302
        assert Specialty.objects.count() == 1
        assert Specialty.objects.first().name == 'test'

    
    @pytest.mark.django_db
    def test_specialty_update_view(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        specialty = Specialty.objects.create(name='test')
        response = client.post(reverse('specialties:specialty_edit', args=[specialty.id]), {'name': 'test_1'})
        assert response.status_code == 302
        specialty.refresh_from_db()
        assert specialty.name == 'test_1'

    @pytest.mark.django_db
    def test_specialty_delete_view(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')
        specialty = Specialty.objects.create(name='test')
        response = client.post(reverse('specialties:specialty_delete', args=[specialty.id]))
        assert response.status_code == 302
        assert Specialty.objects.count() == 0
