from django.urls import path

from Biotics.profiles import views
from Biotics.profiles.views import edit_profile, delete_profile, profile_details

urlpatterns = [
    path('create/', views.BioticsUserRegisterView.as_view(), name='create_profile'),
    path('edit/', edit_profile, name='edit_profile'),
    path('details/', profile_details, name='profile_details'),
    path('delete/', delete_profile, name='delete_profile'),
]
