from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView

from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer

# Create your views here.

class ListCreateEvents(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name"]
    ordering = ["start_time"]


class RegisterAttendee(CreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer

    def get_event(self):
        return get_object_or_404(Event, id=self.kwargs.get("event_id"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["event"] = self.get_event()
        return context


class ListAttendees(ListAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name", "email"]
    ordering = ["name"]
    
    def get_queryset(self):
        return super().get_queryset().filter(event_id=self.kwargs.get("event_id"))

