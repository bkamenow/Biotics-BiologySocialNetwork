from django.urls import path

from Biotics.common.views import home_page

urlpatterns = [
    path('', home_page, name='home_page'),
]

