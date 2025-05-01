from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context: dict[str, str] = {
        'title': 'Панель системы записи - Главная',
    }

    return render(request, 'main/index.html', context)

