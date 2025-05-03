from django.urls import path, re_path
from .views import register, login
from .api import MisAnunciosAPIView

app_name = 'anuncio'
urlpatterns = [
    re_path('api/register', register),
    re_path('api/login', login),
    path('api/mis-anuncios/', MisAnunciosAPIView.as_view())
]
