from django.urls import path, include

from Biotics.events import views
from Biotics.events.views import event_approve, event_deny

urlpatterns = [
    path('', views.EventListView.as_view(), name='events'),
    path('create/', views.EventCreateView.as_view(), name='create_event'),
    path('approve/', views.EventForApproveListView.as_view(), name='approval-event'),
    path('events/approve/<int:pk>/', event_approve, name='event_approve'),
    path('events/deny/<int:pk>/', event_deny, name='event_deny'),
    path('join-event/<int:event_id>/', views.join_event, name='join_event'),
    path('unjoin-event/<int:event_id>/', views.unjoin_event, name='unjoin_event'),
    path('<int:pk>/', include([
        path('', views.EventDetailView.as_view(), name='details-event'),
        path('edit/',  views.EventUpdateView.as_view(), name='edit-event'),
        path('delete/', views.EventDeleteView.as_view(), name='delete-event'),
    ])),
]
