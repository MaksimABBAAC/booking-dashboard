from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView

from appointments.models import Appointment
from masters.models import Master
from .models import Client
from django.urls import reverse_lazy
from .forms import ClientForm
from django.utils import timezone

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('phone_search', '').strip()
        
        if search_query:
            queryset = queryset.filter(
                Q(number__icontains=search_query) |
                Q(tg_id__icontains=search_query)
            )
        return queryset.order_by('number')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('phone_search', '')
        return context

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:clients')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:clients')
    
class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client.html'
    context_object_name = 'client'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = self.object.appointments.select_related('master', 'master__specialty').all()
        return context
    
class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:clients')