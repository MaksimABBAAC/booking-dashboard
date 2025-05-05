from django.urls import path
from .views import WeeklyScheduleCreateView, WeeklyScheduleListView, WeeklyScheduleUpdateView


app_name = 'schedules'

urlpatterns = [
    path('schedules/', WeeklyScheduleListView.as_view(), name='schedules'),
    path('weekly/new/', WeeklyScheduleCreateView.as_view(), name='schedule_add'),
    path('weekly/<int:pk>/edit/', WeeklyScheduleUpdateView.as_view(), name='schedule_edit'),
]