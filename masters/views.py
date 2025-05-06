from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from .forms import MasterForm
from .models import Master
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView


class MasterListView(ListView):
    model = Master
    template_name = 'masters/master_list.html'
    context_object_name = 'masters'
    
    def get_queryset(self):
        return Master.objects.all().order_by()


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
    

class MasterDeleteView(DeleteView):
    model = Master
    template_name = 'masters/master_confirm_delete.html'
    success_url = reverse_lazy('masters:masters')
    
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Мастер успешно удален')
            return response
        except ProtectedError:
            messages.error(
                request,
                'Невозможно удалить специалиста, так как у него есть связанные расписания'
            )
            return redirect('masters:masters')

