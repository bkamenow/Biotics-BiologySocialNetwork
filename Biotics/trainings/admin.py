from django.contrib import admin
from .models import TrainingModel


class TrainingModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'date_of_training', 'type_of_training']
    list_filter = ['type_of_training']
    search_fields = ['title', 'description']


admin.site.register(TrainingModel, TrainingModelAdmin)
