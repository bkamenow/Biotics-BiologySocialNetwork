from django.contrib import admin

from Biotics.events.models import EventModel


# Register your models here.


class EventModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_of_publication', 'event_time', 'duration', 'location', 'user']


admin.site.register(EventModel, EventModelAdmin)
