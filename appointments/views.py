from datetime import timedelta

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, FormView, UpdateView
from phonenumbers import PhoneNumberFormat, format_number, parse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.forms import AppointmentRescheduleForm, BookingForm
from clients.models import Client
from masters.models import Master

from .models import Appointment
from .serializers import AppointmentSerializer


class AvailableAppointmentsList(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        master_id = self.request.query_params.get("master_id")
        date = self.request.query_params.get("date")

        queryset = Appointment.objects.filter(
            is_available=True, date__gte=timezone.now() + timedelta(days=1)
        )

        if master_id:
            queryset = queryset.filter(master_id=master_id)

        if date:
            queryset = queryset.filter(date=date)

        return queryset


class BookAppointmentView(APIView):
    def post(self, request):
        appointment_id = request.data.get("appointment_id")
        phone_number = parse(request.data.get("phone_number"), "RU")
        phone_number = format_number(phone_number, PhoneNumberFormat.E164)
        tg_id = request.data.get("tg_id", None)

        if not appointment_id or not phone_number:
            return Response(
                {"error": "appointment_id and phone_number are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            appointment = Appointment.objects.get(id=appointment_id, is_available=True)

            client, _ = Client.objects.get_or_create(
                number=phone_number, defaults={"tg_id": tg_id} if tg_id else {}
            )

            appointment.client = client
            appointment.is_available = False
            appointment.save()

            return Response({"status": "success"})

        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found or already booked"},
                status=status.HTTP_404_NOT_FOUND,
            )


class BookingView(FormView):
    template_name = "appointments/booking.html"
    form_class = BookingForm
    success_url = reverse_lazy("masters:masters")

    def form_valid(self, form):
        appointment_id = form.cleaned_data["appointment_id"]
        phone_number = parse(form.cleaned_data("phone_number"), "RU")
        phone_number = format_number(phone_number, PhoneNumberFormat.E164)
        tg_id = form.cleaned_data.get("tg_id")

        try:
            appointment = Appointment.objects.get(id=appointment_id, is_available=True)

            tg_id = int(tg_id) if tg_id else None

            client, _ = Client.objects.get_or_create(
                number=phone_number, defaults={"tg_id": tg_id}
            )

            appointment.client = client
            appointment.is_available = False
            appointment.save()

            return super().form_valid(form)

        except Appointment.DoesNotExist:
            self.request.session["booking_form_data"] = {
                "phone_number": self.request.POST.get("phone_number"),
                "tg_id": self.request.POST.get("tg_id"),
            }
            messages.error(self.request, "Это время уже занято, выберите другое")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master_id = self.kwargs.get("master_id")
        context["master"] = Master.objects.get(id=master_id)
        context["available_slots"] = Appointment.objects.filter(
            master_id=master_id,
            is_available=True,
            date__gte=timezone.now() + timedelta(days=1),
        ).order_by("date", "start_time")
        return context


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentRescheduleForm
    template_name = "appointments/appointment_reschedule.html"

    def get_success_url(self):
        client_id = self.original_client_id
        return reverse_lazy("clients:client", kwargs={"pk": client_id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["current_master"] = self.object.master
        self.original_client_id = self.object.client.pk if self.object.client else None
        return kwargs

    def form_valid(self, form):
        old_appointment = self.object
        new_slot = form.cleaned_data["new_slot"]

        if not new_slot.is_available:
            form.add_error("new_slot", "Этот слот уже занят")
            return self.form_invalid(form)

        new_slot.client = old_appointment.client
        new_slot.is_available = False
        new_slot.save()

        old_appointment.client = None
        old_appointment.is_available = True
        old_appointment.save()

        messages.success(self.request, "Запись успешно перенесена")
        return super().form_valid(form)


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = "appointments/appointment_confirm_delete.html"
    success_url = reverse_lazy("clients:clients")
