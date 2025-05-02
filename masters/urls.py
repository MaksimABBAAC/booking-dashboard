from django.urls import path
from masters import views
from .views import ScheduleCreateView, ScheduleUpdateView

app_name = 'masters'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('<int:pk>/', views.master, name='master'),
    path('schedule/add/', ScheduleCreateView.as_view(), name='schedule_add'),
    path('schedule/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_edit'),
]
