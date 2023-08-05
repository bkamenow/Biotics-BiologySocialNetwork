from django.core.validators import MinLengthValidator
from django.db import models

from Biotics.profiles.models import BioticsUserModel


class EventModel(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=300, validators=(MinLengthValidator(10),), blank=False, null=False)
    date_of_publication = models.DateField(auto_now=True)
    event_time = models.TimeField(blank=True, null=True)
    duration = models.CharField(blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(to=BioticsUserModel, on_delete=models.CASCADE, related_name='events')
    is_approved = models.BooleanField(default=False)
