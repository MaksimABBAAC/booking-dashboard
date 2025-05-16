from .forms import MasterForm
from .models import Master
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MasterSerializer

class MasterListView(ListView):
    model = Master
    template_name = 'masters/master_list.html'
    context_object_name = 'masters'

class MasterDetailView(DetailView):
    model = Master
    template_name = 'masters/master.html'
    context_object_name = 'master'

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
    
class MasterDeleteView(DeleteView):
    model = Master
    template_name = 'masters/master_confirm_delete.html'
    success_url = reverse_lazy('masters:masters')



class APImaster(generics.ListAPIView):
    serializer_class = MasterSerializer

    def get_queryset(self):
        queryset = Master.objects.filter()

        return queryset
