from django.urls import path

from .views import (AppointmentDeleteView, AppointmentUpdateView,
                    AvailableAppointmentsList, BookAppointmentView,
                    BookingView)

app_name = "appointments"

urlpatterns = [
    path("book/<int:master_id>/", BookingView.as_view(), name="booking"),
    path(
        "available/", AvailableAppointmentsList.as_view(), name="available-appointments"
    ),
    path("book/", BookAppointmentView.as_view(), name="book-appointment"),
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
]
