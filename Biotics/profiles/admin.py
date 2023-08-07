from django.contrib import admin

from Biotics.profiles.models import BioticsUserModel


class BioticsUserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'gender', 'biology_type', 'rank', 'age']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['gender', 'biology_type', 'rank']


admin.site.register(BioticsUserModel, BioticsUserModelAdmin)
