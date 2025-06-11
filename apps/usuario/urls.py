from django.contrib import admin
from django.urls import path, re_path
from apps.usuario.api.views import register, login
from .api.views import perfil

app_name = 'usuario'
urlpatterns = [
    re_path('api/register', register, name='auth_url_register'),
    re_path('api/login', login, name='auth_url_login'),
    path('api/perfil', perfil),
]