from django.urls import path

from .views import (ClientCreateView, ClientDeleteView, ClientDetailView,
                    ClientListView, ClientUpdateView)

app_name = "clients"

urlpatterns = [
    path("clients/", ClientListView.as_view(), name="clients"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client"),
    path("client/add/", ClientCreateView.as_view(), name="client_add"),
    path("client/<int:pk>/edit/", ClientUpdateView.as_view(), name="client_edit"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
