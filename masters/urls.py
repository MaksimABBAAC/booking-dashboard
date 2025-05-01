from django.urls import path
from masters import views

app_name = 'masters'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('<int:pk>/', views.master, name='master'),
]
