from django.urls import path
from .api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView

app_name = 'anuncio'
urlpatterns = [
    path('api/categoria/', CategoriaListaAPIView.as_view()),
    path('api/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('api/anuncio/', AnuncioListaAPIView.as_view()),
    path('api/anuncio/<pk>/', AnuncioDetalleAPIView.as_view()),
]
