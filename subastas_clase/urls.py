from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from apps.anuncio.api.viewset import AnuncioViewSet, CategoriaViewSet

# Initializar el router de DRF solo una vez
router = routers.DefaultRouter()

# Registrar un ViewSet
router.register(prefix='categoria', viewset=CategoriaViewSet)
router.register(prefix='anuncio', viewset=AnuncioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.anuncio.urls', namespace='anuncios')),
    path('', include('apps.usuario.urls', namespace='usuario')),
    path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
]
