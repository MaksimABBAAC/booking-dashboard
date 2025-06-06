from typing import Any
from django.views.generic import DeleteView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from .models import WeeklySchedule, DailySchedule
from .forms import WeeklyScheduleCreateForm, DailyScheduleForm


class WeeklyScheduleListView(ListView):
    model = WeeklySchedule
    template_name = 'schedules/weekly_schedule_list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return WeeklySchedule.objects.select_related('master').order_by('-id')

class WeeklyScheduleDeleteView(DeleteView):
    model = WeeklySchedule
    template_name = 'schedules/schedules_confirm_delete.html'
    success_url = reverse_lazy('schedules:schedules')

class BaseWeeklyScheduleView:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            is_post = self.request.method == 'POST'

            context['daily_forms'] = self.get_daily_forms(
                weekly_schedule = getattr(self, 'object', None),
                is_post=is_post
            )

            return context

    def get_daily_forms(self, weekly_schedule=None, is_post=False):
        daily_forms=[]
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'

            instance = None
            if weekly_schedule:
                instance = DailySchedule.objects.filter(
                    weekly_schedule = weekly_schedule,
                    day_of_week = day_num
                ).first()

            form_data = self.request.POST if is_post else None
            day_form = DailyScheduleForm(form_data, prefix=prefix, instance=instance)
            daily_forms.append((day_name, day_form))
        
        return daily_forms
    
    def validate_dayly_forms(self, daily_forms):
        for _, form in daily_forms:
            if form.data.get(f'{form.prefix}-is_working') == 'on':
                if not form.is_valid():
                    return False
        return True
    
    def save_daily_forms(self, weekly_schedule):
        for day_num, _ in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            instance = DailySchedule.objects.filter(
                weekly_schedule = weekly_schedule,
                day_of_week = day_num
            ).first()
            
            day_form = DailyScheduleForm(
                self.request.POST,
                prefix=prefix,
                instance=instance
            )

        if day_form.is_valid():
            day_instance = day_form.save(commit=False)
            day_instance.weekly_schedule = weekly_schedule
            day_instance.day_of_week = day_num
            day_instance.save()

    def from_valid(self, form):
        self.object = form.save(commit=False)
        daily_forms = self.get_daily_forms(
            weekly_schedule=self.object,
            is_post=True
        )

        if not self.validate_daily_forms(daily_forms):
            return self.render_to_response(
                self.get_context_data(form=form, daily_forms=daily_forms)
            )
        
        self.object.save()
        self.save_daily_forms(self.object)

        return super().form_valid(form)

class WeeklyScheduleCreateView(BaseWeeklyScheduleView, CreateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleCreateForm 
    template_name = 'schedules/weekly_schedule_form.html'
    success_url = reverse_lazy('schedules:schedules')

class WeeklyScheduleUpdateView(BaseWeeklyScheduleView, UpdateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleCreateForm 
    template_name = 'schedules/weekly_schedule_form.html'
    success_url = reverse_lazy('schedules:schedules')
