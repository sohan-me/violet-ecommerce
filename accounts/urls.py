from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('account-login/', views.Log_In, name ='login'),
    path('account-logout/', views.Log_Out, name='logout'),
    path('account-register/', views.Sign_Up, name='signup'),
    path('reset-password/', views.Reset_Password, name='reset_password'),

    path('activate/<uidb64>/<token>/', views.Activate, name='activate'),
    path('reset_password_validate/<uidb64>/<token>/', views.Reset_Password_Validate, name='reset_password_validate'),
    path('reset_password_process/', views.Reset_Password_Process, name='reset_password_process'),
    path('change_password/', views.Change_Password, name='change_password'),

    path('account-user-profile/', views.DashBoard, name='dashboard'),
    path('update-profile/', views.Update_Profile, name='update_profile'),
]