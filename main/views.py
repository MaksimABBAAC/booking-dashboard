from django.shortcuts import render


def index(request):
    context: dict[str, str] = {
        "title": "Панель системы записи - Главная",
    }

    return render(request, "main/index.html", context)
