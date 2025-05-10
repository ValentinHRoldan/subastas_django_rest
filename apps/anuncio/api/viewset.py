from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer, OfertaAnuncioSerializer
from rest_framework.decorators import action
import datetime
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import CategoriaFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    permission_classes = [DjangoModelPermissions]
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
    queryset = Anuncio.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
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

    def list(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        if version == "1":
            return Response({"mensaje": f"Estas en una version vieja: version {version}"})
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        anuncio = self.get_object()
        if anuncio.publicado_por != request.user:
            return Response({'detail': 'No tienes permiso para eliminar este anuncio.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        anuncio = self.get_object()
        if anuncio.publicado_por != request.user:
            return Response({'detail': 'No tienes permiso para actualizar este anuncio.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        anuncio = self.get_object()
        if anuncio.publicado_por != request.user:
            return Response({'detail': 'No tienes permiso para modificar este anuncio.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
    
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
    
    @action(detail=True, methods=['post'])
    # def ofertar(self, request, pk=None):

    #     anuncio = self.get_object()
    #     diccionario_of_anuncio = {"anuncio":anuncio, "precio_oferta" :request.data['precio_oferta'], "usuario": request.user}

    #     oferta_anuncio = OfertaAnuncio(**diccionario_of_anuncio)

    #     serializer = OfertaAnuncioSerializer(oferta_anuncio,data=request.data)

    #     if serializer.is_valid():
    #         oferta_anuncio.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def ofertar(self, request, pk=None):
        anuncio = self.get_object()
        
        if anuncio.publicado_por == request.user:
            return Response({
                'Error': "No podés ofertar sobre tu propio anuncio"
            })
        
        data = {
            "precio_oferta": request.data.get('precio_oferta')
        }

        serializer = OfertaAnuncioSerializer(data=data)
        if serializer.is_valid():
            serializer.save(usuario=request.user, anuncio=anuncio)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

