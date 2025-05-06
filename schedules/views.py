from django.http import Http404
from django.views.generic import DeleteView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from .models import WeeklySchedule, DailySchedule
from .forms import WeeklyScheduleCreateForm, DailyScheduleForm


class WeeklyScheduleListView(ListView):
    model = WeeklySchedule
    template_name = 'schedules/weekly_schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 10

    def get_queryset(self):
        return WeeklySchedule.objects.select_related('master').order_by('-id')



class WeeklyScheduleCreateView(CreateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleCreateForm
    template_name = 'schedules/weekly_schedule_form.html'
    success_url = reverse_lazy('schedules:schedules')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        
        daily_forms = []
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            form_data = self.request.POST if self.request.method == 'POST' else None
            day_form = DailyScheduleForm(form_data, prefix=prefix)
            daily_forms.append((day_name, day_form))
        
        context['daily_forms'] = daily_forms
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        valid = True
        daily_forms = []
        
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            day_form = DailyScheduleForm(
                self.request.POST,
                prefix=prefix
            )
            daily_forms.append((day_name, day_form))
            
            if day_form.data.get(f'{prefix}-is_working') == 'on':
                if not day_form.is_valid():
                    valid = False
        
        if not valid:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    daily_forms=daily_forms
                )
            )
        
        self.object.save()
        
        for day_num, _ in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            day_form = DailyScheduleForm(
                self.request.POST,
                prefix=prefix
            )
            
            if day_form.is_valid():
                daily_schedule = day_form.save(commit=False)
                daily_schedule.weekly_schedule = self.object
                daily_schedule.day_of_week = day_num
                daily_schedule.save()
        
        return super().form_valid(form)



class WeeklyScheduleUpdateView(UpdateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleCreateForm
    template_name = 'schedules/weekly_schedule_form.html'
    success_url = reverse_lazy('schedules:schedules')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        
        daily_forms = []
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            instance = DailySchedule.objects.filter(
                weekly_schedule=self.object,
                day_of_week=day_num
            ).first()
            
            form_data = self.request.POST if self.request.method == 'POST' else None
            day_form = DailyScheduleForm(form_data, prefix=prefix, instance=instance)
            daily_forms.append((day_name, day_form))
        
        context['daily_forms'] = daily_forms
        return context

    def form_valid(self, form):
        valid = True
        daily_forms = []
        
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            instance = DailySchedule.objects.filter(
                weekly_schedule=self.object,
                day_of_week=day_num
            ).first()
            
            day_form = DailyScheduleForm(
                self.request.POST,
                prefix=prefix,
                instance=instance
            )
            daily_forms.append((day_name, day_form))
            
            if day_form.data.get(f'{prefix}-is_working') == 'on':
                if not day_form.is_valid():
                    valid = False
        
        if not valid:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    daily_forms=daily_forms
                )
            )
        
        response = super().form_valid(form)
        
        # Сохраняем daily forms
        for day_num, _ in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            instance = DailySchedule.objects.filter(
                weekly_schedule=self.object,
                day_of_week=day_num
            ).first()
            
            day_form = DailyScheduleForm(
                self.request.POST,
                prefix=prefix,
                instance=instance
            )
            
            if day_form.is_valid():
                day_instance = day_form.save(commit=False)
                day_instance.weekly_schedule = self.object
                day_instance.day_of_week = day_num
                day_instance.save()
        
        return response
    
class WeeklyScheduleDeleteView(DeleteView):
    model = WeeklySchedule
    template_name = 'schedules/schedules_confirm_delete.html'
    success_url = reverse_lazy('schedules:schedules')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj:
            raise Http404("Расписание не найдено")
        return obj