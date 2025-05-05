from django.shortcuts import get_list_or_404, get_object_or_404
from .forms import MasterForm
from .models import Master
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView


class MasterListView(ListView):
    model = Master
    template_name = 'masters/master_list.html'
    context_object_name = 'masters'
    
    def get_queryset(self):
        return get_list_or_404(Master)


class MasterCreateView(CreateView):
    model = Master
    form_class = MasterForm
    template_name = 'masters/master_form.html'
    success_url = reverse_lazy('masters:masters')


class MasterUpdateView(UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'masters/master_form.html'
    success_url = reverse_lazy('masters:masters')

    
class MasterDetailView(DetailView):
    model = Master
    template_name = 'masters/master.html'
    context_object_name = 'master'
    pk_url_kwarg = 'pk'
    
    def get_object(self):
        return get_object_or_404(Master, pk=self.kwargs.get('pk'))


