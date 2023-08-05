from django.urls import path

from Biotics.biology.views import zoology_home, botany_home, microbiology_home

urlpatterns = [
    path('zoology/', zoology_home, name='zoology'),
    path('botany/', botany_home, name='botany'),
    path('microbiology/', microbiology_home, name='microbiology'),
]
