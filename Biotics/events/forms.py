from django import forms

from Biotics.events.models import EventModel


class EventForm(forms.ModelForm):
    location_choices = [
        ('afghanistan', 'Afghanistan'),
        ('albania', 'Albania'),
        ('algeria', 'Algeria'),
        ('argentina', 'Argentina'),
        ('australia', 'Australia'),
        ('austria', 'Austria'),
        ('belgium', 'Belgium'),
        ('brazil', 'Brazil'),
        ('bulgaria', 'Bulgaria'),
        ('canada', 'Canada'),
        ('china', 'China'),
        ('croatia', 'Croatia'),
        ('cyprus', 'Cyprus'),
        ('denmark', 'Denmark'),
        ('egypt', 'Egypt'),
        ('france', 'France'),
        ('germany', 'Germany'),
        ('greece', 'Greece'),
        ('hungary', 'Hungary'),
        ('india', 'India'),
        ('ireland', 'Ireland'),
        ('italy', 'Italy'),
        ('japan', 'Japan'),
        ('mexico', 'Mexico'),
        ('netherlands', 'Netherlands'),
        ('norway', 'Norway'),
        ('poland', 'Poland'),
        ('russia', 'Russia'),
        ('spain', 'Spain'),
        ('sweden', 'Sweden'),
        ('thailand', 'Thailand'),
        ('united_kingdom', 'United Kingdom'),
        ('united_states', 'United States'),
    ]
    duration_choices = [
        ('30', '30 minutes'),
        ('60', '1 hour'),
        ('120', '2 hours'),
        ('180', '3 hours'),
        ('240', '4 hours'),
    ]

    location = forms.ChoiceField(choices=location_choices)
    duration = forms.ChoiceField(choices=duration_choices)
    event_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = EventModel
        fields = ['title', 'description', 'event_time', 'duration', 'location']
