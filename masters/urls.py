from django.urls import path
from .views import MasterListView, MasterCreateView, MasterDetailView, MasterUpdateView

app_name = 'masters'

urlpatterns = [
    path('masters/', MasterListView.as_view(), name='masters'),
    path('master/<int:pk>/', MasterDetailView.as_view(), name='master'),
    path('master/add/', MasterCreateView.as_view(), name='master_add'),
    
    path('master/<int:pk>/edit/', MasterUpdateView.as_view(), name='master_edit'),
    # path('schedule/add/', ScheduleCreateView.as_view(), name='schedule_add'),
    # path('schedule/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_edit'),
]
