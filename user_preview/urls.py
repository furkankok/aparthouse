from django.contrib import admin
from django.urls import include, path

from user_preview import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('email-verify', views.email_verify, name='email-verify'),

]
