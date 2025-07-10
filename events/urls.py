from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCreateEvents.as_view(), name="list-create-events"),
    path("<uuid:event_id>/register/", views.RegisterAttendee.as_view(), name="register-attendee"),
    path("<uuid:event_id>/attendees/", views.ListAttendees.as_view(), name="list-attendees"),
]