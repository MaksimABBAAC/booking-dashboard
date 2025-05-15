from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import redirect_to_login

class LoginRequiredMiddleware:
    """
    Middleware для глобальной проверки аутентификации
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = getattr(settings, 'LOGIN_URL', reverse('accounts:login'))
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):
        if not request.user.is_authenticated and not self.is_open_url(request.path):
            
            return redirect_to_login(request.get_full_path(), self.login_url)
        return self.get_response(request)

    def is_open_url(self, path):
        return any(
            path.startswith(url) or (url == '/' and path == '/')
            for url in self.open_urls
        )
