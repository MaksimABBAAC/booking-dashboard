from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("appointments.urls", namespace="appointments")),
    path("", include("clients.urls", namespace="clients")),
    path("", include("main.urls", namespace="main")),
    path("", include("masters.urls", namespace="masters")),
    path("", include("specialties.urls", namespace="specialties")),
    path("", include("schedules.urls", namespace="schedules")),
    path("", include("accounts.urls", namespace="accounts")),
]
