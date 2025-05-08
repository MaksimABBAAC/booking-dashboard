from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from .models import Client
from django.urls import reverse_lazy
from .forms import ClientForm

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    
    def get_queryset(self):
        return Client.objects.all().order_by()
    
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
    pk_url_kwarg = 'pk'
    
    def get_object(self):
        return get_object_or_404(Client, pk=self.kwargs.get('pk'))
    

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'сlients/сlient_confirm_delete.html'
    success_url = reverse_lazy('clients:clients')