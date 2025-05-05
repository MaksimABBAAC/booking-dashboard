from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import WeeklySchedule, DailySchedule
from .forms import WeeklyScheduleCreateForm, DailyScheduleForm

class WeeklyScheduleUpdateView(UpdateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleCreateForm
    template_name = 'schedule/weekly_schedule_form.html'
    success_url = reverse_lazy('schedule:weekly-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['weekly_schedule'] = self.object
        return kwargs

    def form_valid(self, form):
        # Сохраняем данные каждого дня
        for day_num, _ in DailySchedule.DAYS_OF_WEEK:
            prefix = f'day_{day_num}'
            day_form = DailyScheduleForm(
                self.request.POST,
                prefix=prefix,
                instance=DailySchedule.objects.filter(
                    weekly_schedule=self.object,
                    day_of_week=day_num
                ).first()
            )
            if day_form.is_valid():
                day_instance = day_form.save(commit=False)
                day_instance.weekly_schedule = self.object
                day_instance.day_of_week = day_num
                day_instance.save()
        return super().form_valid(form)

class WeeklyScheduleCreateView(CreateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleCreateForm
    template_name = 'schedules/weekly_schedule_create.html'
    success_url = reverse_lazy('schedule:weekly-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        context['daily_forms'] = form.daily_forms
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Создаем записи для каждого дня
        for day_num, day_name in DailySchedule.DAYS_OF_WEEK:
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
        
        return response