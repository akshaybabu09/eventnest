from django.utils import timezone

from django.db import models

class EventManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(start_time__gt=timezone.now())
