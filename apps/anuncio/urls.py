from django.urls import path, re_path
from .api.views import MisAnunciosAPIView

app_name = 'anuncio'
urlpatterns = [
    path('api/mis-anuncios/', MisAnunciosAPIView.as_view())
]
