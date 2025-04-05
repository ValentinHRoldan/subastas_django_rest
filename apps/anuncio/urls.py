from django.urls import path
from .api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView

app_name = 'anuncio'
urlpatterns = [
    path('api/categoria/', CategoriaListaAPIView.as_view()),
    path('api/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('api/anuncios/', AnuncioListaAPIView.as_view()),
]
