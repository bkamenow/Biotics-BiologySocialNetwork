from django.urls import path

from Biotics.common.views import home_page, publications_page, trainings_page, events_page

urlpatterns = [
    path('', home_page, name='home_page'),
    path('publications/', publications_page, name='publications'),
    path('trainings/', trainings_page, name='trainings'),
    path('events/', events_page, name='events'),
]

