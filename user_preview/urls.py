from django.urls import path
from user_preview import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('email-verify', views.email_verify, name='email-verify'),
    path('forget-password', views.forget_password, name='forget-password'),
    path('reset-password', views.reset_password, name='reset-password'),

]
