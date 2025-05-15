from .models import Specialty
from .forms import SpecialtyForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

class SpecialtyListView(ListView):
    model = Specialty
    template_name = 'specialties/specialty_list.html'
    context_object_name = 'specialties'
    
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

class SpecialtyDeleteView(DeleteView):
    model = Specialty
    template_name = 'specialties/specialty_confirm_delete.html'
    success_url = reverse_lazy('specialties:specialties')