from django.urls import path, include

from Biotics.biology import views

urlpatterns = [
    path('zoology/', include([
        path('', views.zoology_home, name='zoology'),
        path('anatomy_and_physiology/', views.anatomy_and_physiology, name='anatomy_and_physiology'),
        path('behavior/', views.behavior, name='behavior'),
        path('conservation/', views.conservation, name='conservation'),
        path('ecology/', views.ecology, name='ecology'),
        path('evolution/', views.evolution, name='evolution'),
        path('genetics/', views.genetics, name='genetics'),
        path('taxonomy_classification/', views.taxonomy_classification, name='taxonomy_classification'),
    ])),
    path('botany/', include([
        path('', views.botany_home, name='botany'),
        path('bacteriology/', views.bacteriology, name='bacteriology'),
        path('environmental_microbiology/', views.environmental_microbiology, name='environmental_microbiology'),
        path('industrial_microbiology/', views.industrial_microbiology, name='industrial_microbiology'),
        path('medical_microbiology/', views.medical_microbiology, name='medical_microbiology'),
        path('microbial_genetics/', views.microbial_genetics, name='microbial_genetics'),
        path('microbial_physiology/', views.microbial_physiology, name='microbial_physiology'),
        path('mycology/', views.mycology, name='mycology'),
        path('protozoology/', views.protozoology, name='protozoology'),
        path('virology/', views.virology, name='virology'),
    ])),
    path('microbiology/', include([
        path('', views.microbiology_home, name='microbiology'),
        path('economic_botany/', views.economic_botany, name='economic_botany'),
        path('ethnobotany/', views.ethnobotany, name='ethnobotany'),
        path('physiology/', views.physiology, name='physiology'),
        path('plant_biotechnology/', views.plant_biotechnology, name='plant_biotechnology'),
        path('plant_ecology/', views.plant_ecology, name='plant_ecology'),
        path('plant_systematics/', views.plant_systematics, name='plant_systematics'),
        path('plantanatomy_morphology/', views.plantanatomy_morphology, name='plantanatomy_morphology'),
        path('plantevolution_genetics/', views.plantevolution_genetics, name='plantevolution_genetics'),
        path('taxonomy_systematics/', views.taxonomy_systematics, name='taxonomy_systematics'),
    ])),
]
