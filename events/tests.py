from django.utils import timezone
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Event, Attendee

import datetime


class EventTests(APITestCase):
    def setUp(self):
        self.start_time = timezone.now() + datetime.timedelta(hours=1)
        self.end_time = timezone.now() + datetime.timedelta(hours=2)
        self.url = reverse("list-create-events")
        self.event_data = {
            "name": "Tech Meetup",
            "location": {
                "type": "Point",
                "coordinates": [77.546369, 13.114601]
            },
            "address": "Bangalore, India",
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "max_capacity": 100
        }

    def test_create_event_success(self):
        response = self.client.post(self.url, self.event_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

    def test_create_event_in_past(self):
        start_time = timezone.now() - datetime.timedelta(hours=1)
        self.event_data["start_time"] = start_time.isoformat()
        response = self.client.post(self.url, self.event_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Start time must be in the future", str(response.data))

    def test_create_event_with_end_before_start(self):
        self.event_data["end_time"] = self.start_time - datetime.timedelta(minutes=30)
        response = self.client.post(self.url, self.event_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("End time must be after start time", str(response.data))

    def test_event_overlap_same_location(self):
        # First event
        self.client.post(self.url, self.event_data, format="json")
        # Overlapping second event
        overlapping_data = self.event_data.copy()
        overlapping_data["name"] = "Overlap Event"
        response = self.client.post(self.url, overlapping_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Another event is scheduled", str(response.data))


class AttendeeTests(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            location=Point(10.0, 20.0),
            address="Test Address",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=1, hours=2),
            max_capacity=2
        )
        self.attendee_data = {
            "name": "Alice",
            "email": "alice@example.com"
        }

    def test_register_attendee_success(self):
        url = reverse("register-attendee", kwargs={"event_id": str(self.event.id)})
        response = self.client.post(url, self.attendee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.event.attendees.count(), 1)

    def test_register_duplicate_attendee(self):
        Attendee.objects.create(event=self.event, name="Alice", email="alice@example.com")
        url = reverse("register-attendee", kwargs={"event_id": str(self.event.id)})
        response = self.client.post(url, self.attendee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already registered", str(response.data))

    def test_register_attendee_event_full(self):
        # Fill event to capacity
        Attendee.objects.create(event=self.event, name="A", email="a@example.com")
        Attendee.objects.create(event=self.event, name="B", email="b@example.com")

        url = reverse("register-attendee", kwargs={"event_id": str(self.event.id)})
        response = self.client.post(url, self.attendee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("maximum capacity", str(response.data))


class ListingTests(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="List Event",
            location=Point(10.0, 20.0),
            address="Event Address",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=1, hours=2),
            max_capacity=50
        )
        Attendee.objects.create(event=self.event, name="John", email="john@example.com")

    def test_list_events(self):
        url = reverse("list-create-events")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data.get("count"), 1)

    def test_list_attendees(self):
        url = reverse("list-attendees", kwargs={"event_id": str(self.event.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
