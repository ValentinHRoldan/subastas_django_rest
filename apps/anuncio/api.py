from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer
from apps.usuario.models import Usuario
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import action
import datetime


class CategoriaListaAPIView(APIView):
    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetalleAPIView(APIView):
    def get(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# endpoints con vistas genericas y viewsets (para categorias)  

class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ---------------------------------------------------
    
class AnuncioListaAPIView(APIView):
    def get(self, request):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)  

    def post(self, request):
        serializer = AnuncioSerializer(data=request.data)
        if not(serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #simulacion del usuario autenticado
        fakeUser = Usuario.objects.get(id = 1)
        serializer.save(publicado_por=fakeUser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AnuncioDetalleAPIView(APIView):
    def get(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# endpoints con vistas genericas y viewsets (para anuncios)  

class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    def perform_create(self, serializer):
        fakeUser = Usuario.objects.get(id = 1)
        serializer.save(publicado_por=fakeUser)

class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

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

# ---------------------------------------------------