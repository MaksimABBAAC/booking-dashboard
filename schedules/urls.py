from django.urls import path
from .views import WeeklyScheduleCreateView, WeeklyScheduleUpdateView


app_name = 'schedules'

urlpatterns = [
    path('weekly/new/', WeeklyScheduleCreateView.as_view(), name='weekly-create'),
    path('weekly/<int:pk>/edit/', WeeklyScheduleUpdateView.as_view(), name='weekly-edit'),
]