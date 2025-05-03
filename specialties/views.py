from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Specialty
from .forms import SpecialtyForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

class SpecialtyListView(ListView):
    model = Specialty
    template_name = 'specialties/specialty_list.html'
    context_object_name = 'specialties'
    
    def get_queryset(self):
        return get_list_or_404(Specialty)
    
class SpecialtyCreateView(CreateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = 'specialties/specialty_form.html'
    success_url = reverse_lazy('specialties:specialties')

class SpecialtyUpdateView(UpdateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = 'specialties/specialty_form.html'
    success_url = reverse_lazy('specialties:specialties')
