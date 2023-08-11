from django.urls import path, include

from Biotics.publications import views

urlpatterns = [
    path('', views.PublicationListView.as_view(), name='publications'),
    path('create/', views.PublicationCreateView.as_view(), name='create_publication'),
    path('<int:pk>/', include([
        path('', views.PublicationDetailView.as_view(), name='details-publication'),
        path('edit/',  views.PublicationUpdateView.as_view(), name='edit-publication'),
        path('delete/', views.PublicationDeleteView.as_view(), name='delete-publication'),
        path('like/', views.like_publication, name='like-publication'),
        path('comment/', views.add_comment, name='add-comment'),
    ])),
    path('<str:filter_type>/', views.FilteredPublicationsListView.as_view(), name='filtered_publications'),

]
