from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from Biotics.events.forms import EventForm
from Biotics.events.models import EventModel, BioticsUserModel
from Biotics.events.views import event_approve, event_deny, unjoin_event, join_event


class EventModelTestCase(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(username='bobi111', email='bobi1@example.com', password='bobi123')

    def test_create_event(self):
        event = EventModel.objects.create(
            title='Test Event',
            description='This is a test event description.',
            location='Test Location',
            user=self.user,
        )

        self.assertEqual(EventModel.objects.count(), 1)
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.description, 'This is a test event description.')
        self.assertEqual(event.location, 'Test Location')
        self.assertFalse(event.is_approved)
        self.assertEqual(event.participants.count(), 0)


class EventFormTestCase(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(username='bobi111', email='bobi1@example.com', password='bobi123')

    def test_valid_event_form(self):
        form_data = {
            'title': 'Test Event',
            'description': 'This is a test event description.',
            'event_time': '15:30',
            'duration': '60',
            'location': 'united_states',
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_event_form(self):
        form_data = {
            'title': 'Test Event',
            'description': 'This is a test event description.',
            'event_time': '15:30',
            # 'duration' and 'location' fields are missing
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test invalid event_time format
        form_data['duration'] = '60'
        form_data['location'] = 'united_states'
        form_data['event_time'] = 'invalid_time'
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test invalid duration value
        form_data['event_time'] = '15:30'
        form_data['duration'] = 'invalid_duration'
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())


class EventCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BioticsUserModel.objects.create_user(
            username='bobi1',
            password='bobi123'
        )
        self.login_url = reverse('login_page')
        self.create_event_url = reverse('create_event')  # Replace with your actual URL name

    def test_event_create_view_authenticated(self):
        self.client.login(username='bobi1', password='bobi123')

        response = self.client.get(self.create_event_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create-event.html')

        form_data = {
            'title': 'Test Event',
            'description': 'This is a test event.',
            'location': 'united_states',
            'duration': '60',
            'event_time': '12:00',
        }
        response = self.client.post(self.create_event_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(EventModel.objects.count(), 1)

        event = EventModel.objects.first()
        self.assertEqual(event.user, self.user)


class EventApprovalViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = BioticsUserModel.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.user = BioticsUserModel.objects.create_user(username='regular_user', email='user@example.com', password='userpass')
        self.event = EventModel.objects.create(title='Test Event', description='A test event', user=self.user)
        self.approve_url = reverse('event_approve', kwargs={'pk': self.event.pk})
        self.deny_url = reverse('event_deny', kwargs={'pk': self.event.pk})

    def test_event_approve_view(self):
        request = self.factory.post(self.approve_url)
        request.user = self.superuser
        response = event_approve(request, pk=self.event.pk)
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertTrue(self.event.is_approved)

    def test_event_deny_view(self):
        request = self.factory.post(self.deny_url)
        request.user = self.superuser
        response = event_deny(request, pk=self.event.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(EventModel.objects.filter(pk=self.event.pk).exists())

