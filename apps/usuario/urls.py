from django.contrib import admin
from django.urls import path

from .api.views import perfil

app_name = 'usuario'
urlpatterns = [
    path('api/perfil', perfil),
]