from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer
from apps.usuario.models import Usuario

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