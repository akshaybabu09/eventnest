from django.contrib import admin

from .models import Event, Attendee
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "end_time",
        "address",
        "max_capacity"
    )
    search_fields = ("name",)

class AttendeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "event"
    )
    search_fields = ("event_id", "name", "email")


admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, AttendeeAdmin)
