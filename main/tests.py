import pytest
from django.contrib.auth.models import User
from django.urls import reverse


class TestIndex:
    @pytest.mark.django_db
    def test_index_view_status_code(self, client):
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        url = reverse("main:index")
        response = client.get(url)
        assert response.status_code == 200
        assert "title" in response.context
        assert response.context["title"] == "Панель системы записи - Главная"
        assert "main/index.html" in (t.name for t in response.templates)
