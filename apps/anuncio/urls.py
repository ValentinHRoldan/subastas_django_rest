from django.urls import path, re_path, include
from .views import register, login

app_name = 'anuncio'
urlpatterns = [
    re_path('register', register),
    re_path('login', login),
]
