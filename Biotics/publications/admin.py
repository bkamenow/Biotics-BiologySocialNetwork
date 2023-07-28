from django.contrib import admin

from Biotics.publications.models import PublicationModel


# Register your models here.


class PublicationModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'date_of_publication', 'user']
    search_fields = ['title', 'user__username']
    list_filter = ['type_of_publication', 'date_of_publication']


admin.site.register(PublicationModel, PublicationModelAdmin)
