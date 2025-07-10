import uuid
from django.db import models
from django.contrib.gis.db import models as gis_model

from .managers import EventManager
from library.base_models import TimeStampedModel

# Create your models here.

class Event(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    location = gis_model.PointField()
    address = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()

    objects = EventManager()

    class Meta:
        ordering = ["start_time"]
        constraints = [
                models.UniqueConstraint(
                    fields=["name", "location", "start_time", "end_time"],
                    name="unique_event_with_location_and_time"
                )
            ]


    def __str__(self):
        return self.name

    def attendee_count(self):
        return self.attendees.count()
    
    def has_space(self):
        return self.max_capacity > self.attendee_count()
    
    @classmethod
    def events_by_location(cls, location):
        return cls.objects.filter(location=location)


class Attendee(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    email = models.EmailField()
    event = models.ForeignKey('Event', related_name="attendees", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        ordering = ["name"]
        constraints = [
                models.UniqueConstraint(
                    fields=["event", "email"],
                    name="unique_event_and_email"
                )
            ]

