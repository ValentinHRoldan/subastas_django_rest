from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer
from apps.usuario.models import Usuario
from rest_framework.decorators import action
import datetime
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoriaFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    #para filtros
    filterset_fields = ['nombre','activa']

    #para orden
    ordering_fields = ['nombre', 'id']

    def list(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        if version == "1":
            return Response({"mensaje": f"Estas en una version vieja: version {version}"})
        return super().list(request, *args, **kwargs)

class AnuncioViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    #para filtros
    filterset_fields = ['categorias','activo']

    #para orden
    ordering_fields = ['titulo', 'fecha_fin', 'precio_inicial', 'fecha_publicacion']

    def perform_create(self, serializer):
        usuario = self.request.user
        serializer.save(publicado_por=usuario)

    @action(detail=True, methods=['get'])
    def tiempo_restante(self, request, pk=None):
        # Se obtiene la instancia de Usuario de acuerdo al ‘pk’ enviado en la url
        anuncio = self.get_object()
        serializer = AnuncioSerializer(anuncio)

        fecha_actual = datetime.datetime.now().replace(tzinfo=None)
        tiempo_restante = anuncio.fecha_fin.replace(tzinfo=None) - fecha_actual
        total_segundos = abs(tiempo_restante.total_seconds())
        horas = int((total_segundos % 86400) // 3600)
        minutos = int((total_segundos % 3600) // 60)
        
        return Response({'tiempo_restante':{'dias': tiempo_restante.days, 'horas': horas, 'minutos': minutos}})

    def list(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        if version == "1":
            return Response({"mensaje": f"Estas en una version vieja: version {version}"})
        return super().list(request, *args, **kwargs)
# ---------------------------------------------------
