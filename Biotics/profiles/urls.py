from django.urls import path

from Biotics.profiles import views

urlpatterns = [
    path('create/', views.BioticsUserRegisterView.as_view(), name='create_profile'),
    path('login/', views.BioticsUserLoginView.as_view(), name='login_page'),
    path('logout/', views.BioticsUserLogoutView.as_view(), name='logout_user'),
    path('edit/<int:pk>/', views.BioticsUserEditView.as_view(), name='edit_profile'),
    path('details/<int:pk>/', views.BioticsUserDetailsView.as_view(), name='profile_details'),
    path('delete/<int:pk>/', views.BioticsUserDeleteView.as_view(), name='delete_profile'),

    path('reset_password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]
