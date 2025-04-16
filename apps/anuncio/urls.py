from django.urls import path
from .api import AnuncioDetalleGenericView, AnuncioListaGenericView, CategoriaDetalleGenericView, CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView, CategoriaListaGenericView

app_name = 'anuncio'
urlpatterns = [
    path('api/categoria/', CategoriaListaAPIView.as_view()),
    path('api/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('api/anuncio/', AnuncioListaAPIView.as_view()),
    path('api/anuncio/<pk>/', AnuncioDetalleAPIView.as_view()),
    path('generic-view/categoria/', CategoriaListaGenericView.as_view()),
    path('generic-view/categoria/<int:pk>/', CategoriaDetalleGenericView.as_view()),
    path('generic-view/anuncio/', AnuncioListaGenericView.as_view()),
    path('generic-view/anuncio/<int:pk>/', AnuncioDetalleGenericView.as_view()),
]
