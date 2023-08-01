from django.urls import path

from Biotics.trainings import views

urlpatterns = [
    path('', views.TrainingListView.as_view(), name='trainings'),
    path('create/', views.TrainingCreateView.as_view(), name='create_training'),
    path('edit/<int:pk>/', views.TrainingUpdateView.as_view(), name='edit_training'),
    path('delete/<int:pk>/', views.TrainingDeleteView.as_view(), name='delete_training'),
    path('join_training/<int:pk>/', views.join_training, name='join_training'),

]
