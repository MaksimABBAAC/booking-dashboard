from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from .forms import MasterForm, ScheduleForm
from .models import Master, Schedule
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

def index(request):
    masters = get_list_or_404(Master)

    return render(request, 'masters/index.html', {'masters': masters})

def add(request):
    if request.method == 'POST':
        form = MasterForm(request.POST)
        if form.is_valid():
            master = form.save()
            return redirect('masters:master', pk=master.pk)
    else:
        form = MasterForm()
        
    return render(request, 'masters/add.html', {'form': form})
    
def master(request, pk):
    master = get_object_or_404(Master, pk=pk)
    return render(request, 'masters/master.html', {'master': master})

class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'masters/schedule.html'
    success_url = reverse_lazy('schedule_list')

class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'masters/schedule.html'
    success_url = reverse_lazy('schedule_list')