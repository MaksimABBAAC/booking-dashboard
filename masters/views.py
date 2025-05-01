from django.shortcuts import redirect, render, get_object_or_404
from .forms import AddMasterForm
from .models import Masters

def index(request):
    context: dict[str, str] = {
        'title': 'Панель системы записи - Мастера',
    }

    return render(request, 'masters/index.html', context)

def add(request):
    if request.method == 'POST':
        form = AddMasterForm(request.POST)
        if form.is_valid():
            master = form.save()
            return redirect('masters:master', pk=master.pk)
    else:
        form = AddMasterForm()
        
    return render(request, 'masters/add.html', {'form': form})
    
def master(request, pk):
    master = get_object_or_404(Masters, pk=pk)
    return render(request, 'masters/master.html', {'master': master})