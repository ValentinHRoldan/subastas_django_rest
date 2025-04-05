from django.urls import path
from .api import CategoriaListaAPIView, CategoriaDetalleAPIView

app_name = 'anuncio'
urlpatterns = [
    path('api/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
]
