from django.urls import path, include

from Biotics.events import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='events'),
    path('create/', views.EventCreateView.as_view(), name='create_event'),
    path('<int:pk>/', include([
        path('', views.EventDetailView.as_view(), name='details-event'),
        path('edit/',  views.EventUpdateView.as_view(), name='edit-event'),
        path('delete/', views.EventDeleteView.as_view(), name='delete-event'),
    ]))
]
