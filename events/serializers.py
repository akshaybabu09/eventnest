from django.utils import timezone
from rest_framework import serializers

from .models import Event, Attendee

class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    class Meta:
        model = Event
        fields = ["id", "name", "location", "address", "start_time", "end_time", "max_capacity"]
        read_only_fields = ["id"]
    
    def validate(self, attrs):
        location = attrs.get("location")
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if start_time < timezone.now():
            raise serializers.ValidationError("Start time must be in the future.")
        
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        # checking if 
        # existing event starts before the new event ends
        # existing event ends after the new event starts
        overlapping_events = Event.objects.filter(
            location=location,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if overlapping_events.exists():
            raise serializers.ValidationError("Another event is scheduled for the given location and time")
        return attrs



class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email', 'event']
        read_only_fields = ['id', 'event']

    
    def validate(self, attrs):
        event = self.context.get("event")
        email = attrs.get("email")

        if Attendee.objects.filter(event=event, email=email).exists():
            raise serializers.ValidationError("This email is already registered for the event.")
        
        if not event.has_space():
            raise serializers.ValidationError("The event has reached its maximum capacity.")
        
        attrs["event"] = event
        return attrs
    