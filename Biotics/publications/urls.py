from django.urls import path

from Biotics.publications.views import publications_page, create_publication

urlpatterns = [
    path('', publications_page, name='publications'),
    path('create/', create_publication, name='create_publication'),
]
