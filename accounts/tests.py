import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestAuthViews:

    def test_login_view_get(self, client):
        url = reverse("accounts:login")
        response = client.get(url)
        assert response.status_code == 200
        assert "accounts/login.html" in (t.name for t in response.templates)

    def test_login_view_post_valid(self, client):
        username = "testuser"
        password = "testpassword"
        User.objects.create_user(username=username, password=password)

        url = reverse("accounts:login")
        response = client.post(url, {"username": username, "password": password})
        assert response.status_code == 302
        response = client.get(reverse("main:index"))
        assert response.wsgi_request.user.is_authenticated

    def test_login_view_post_invalid(self, client):
        url = reverse("accounts:login")
        response = client.post(url, {"username": "no_user", "password": "bad"})

        assert response.status_code == 200
        form = response.context.get("form")
        assert form is not None
        assert form.errors

    def test_logout_view(self, client, django_user_model):
        user = django_user_model.objects.create_user(
            username="testuser", password="pass"
        )
        client.login(username="testuser", password="pass")

        url = reverse("accounts:logout")
        response = client.post(url)
        assert response.status_code == 302

        response = client.get(reverse("main:index"))
        assert not response.wsgi_request.user.is_authenticated
