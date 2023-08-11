from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import EventModel
from .views import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDetailView,
    EventDeleteView,
    event_approve,
    event_deny,
    join_event,
    unjoin_event,
)
from ..profiles.models import BioticsUserModel


class EventViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BioticsUserModel.objects.create_user(username='bobi123', password='Sometestpass1',email='bobi@abv.bg')
        self.superuser = BioticsUserModel.objects.create_superuser(username='bobi111', password='Sometestpass1', email='bobi@abv.bg')
        self.event = EventModel.objects.create(title='Test Event', description='A test event')

    def test_event_list_view(self):
        request = self.factory.get(reverse('events'))
        request.user = self.user
        response = EventListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_event_create_view(self):
        request = self.factory.get(reverse('event-create'))
        request.user = self.user
        response = EventCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_event_approve_view(self):
        url = reverse('event-approve', args=[self.event.pk])
        request = self.factory.post(url)
        request.user = self.superuser
        response = event_approve(request, self.event.pk)
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertTrue(self.event.is_approved)

    def test_join_event(self):
        url = reverse('join-event', args=[self.event.pk])
        request = self.factory.get(url)
        request.user = self.user
        response = join_event(request, self.event.pk)
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertTrue(self.user in self.event.participants.all())



