from django.urls import path
from .views import SpecialtyDeleteView, SpecialtyListView, SpecialtyCreateView, SpecialtyUpdateView

app_name = 'specialties'

urlpatterns = [
    path('specialties/', SpecialtyListView.as_view(), name='specialties'),
    path('specialty/add/', SpecialtyCreateView.as_view(), name='specialty_add'),
    path('specialty/<int:pk>/edit/', SpecialtyUpdateView.as_view(), name='specialty_edit'),
    path('specialty/<int:pk>/delete/', SpecialtyDeleteView.as_view(), name='specialty_delete'),
]