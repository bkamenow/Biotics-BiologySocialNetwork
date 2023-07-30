from django import forms

from Biotics.events.models import EventModel


class EventForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = ['title', 'description', 'event_time', 'duration', 'location']
