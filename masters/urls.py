from django.urls import path

from .views import (APImaster, MasterCreateView, MasterDeleteView,
                    MasterDetailView, MasterListView, MasterUpdateView)

app_name = "masters"

urlpatterns = [
    path("API/masters/", APImaster.as_view(), name="api_masters"),
    path("masters/", MasterListView.as_view(), name="masters"),
    path("master/<int:pk>/", MasterDetailView.as_view(), name="master"),
    path("master/add/", MasterCreateView.as_view(), name="master_add"),
    path("master/<int:pk>/edit/", MasterUpdateView.as_view(), name="master_edit"),
    path("master/<int:pk>/delete/", MasterDeleteView.as_view(), name="master_delete"),
]
