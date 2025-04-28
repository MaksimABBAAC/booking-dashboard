from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request)-> HttpResponse:
    
    context: dict[str, str] = {
        'title': 'Home',
        'content': 'Main page'
    }

    return render(request, 'main/index.html', context)
