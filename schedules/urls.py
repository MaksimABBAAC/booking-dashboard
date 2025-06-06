from django.urls import path
from .views import WeeklyScheduleCreateView, WeeklyScheduleDeleteView, WeeklyScheduleListView, WeeklyScheduleUpdateView


app_name = 'schedules'

urlpatterns = [
    path('schedules/', WeeklyScheduleListView.as_view(), name='schedules'),
    path('schedule/add/', WeeklyScheduleCreateView.as_view(), name='schedule_add'),
    path('schedule/<int:pk>/edit/', WeeklyScheduleUpdateView.as_view(), name='schedule_edit'),
    path('schedule<int:pk>/delete/',  WeeklyScheduleDeleteView.as_view(), name='schedule_delete'),
]
