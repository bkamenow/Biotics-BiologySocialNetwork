from django.urls import path
from Biotics.messaging import views

urlpatterns = [
    path('conversations/', views.conversations_list, name='conversations_list'),
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation_view'),
    path('messaging/create-conversation/<int:other_user_id>/', views.create_conversation, name='create_conversation'),
]
