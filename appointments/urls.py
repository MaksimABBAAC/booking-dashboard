from django.urls import path

from .views import (AppointmentDeleteView, AppointmentUpdateView,
                    AvailableAppointmentsList, BookAppointmentView,
                    BookingView, BookedAppointmentsByTgId, CancelAppointmentView)

app_name = "appointments"

urlpatterns = [
    path("book/<int:master_id>/", BookingView.as_view(), name="booking"),
    path(
        "API/available/", AvailableAppointmentsList.as_view(), name="available-appointments"
    ),
    path("API/book/", BookAppointmentView.as_view(), name="book-appointment"),
    path("API/booking/", BookedAppointmentsByTgId.as_view(), name="booking-notavailable"),
    path("API/appointment/delete", CancelAppointmentView().as_view(), name="cancel-booking"),
    path(
        "appointments/<int:pk>/edit/",
        AppointmentUpdateView.as_view(),
        name="appointment_edit",
    ),
    path(
        "appointments/<int:pk>/delete/",
        AppointmentDeleteView.as_view(),
        name="appointment_delete",
    ),
    path(
        "appointments/<int:pk>/delete/",
        AppointmentDeleteView.as_view(),
        name="appointment_delete",
    ),
]
