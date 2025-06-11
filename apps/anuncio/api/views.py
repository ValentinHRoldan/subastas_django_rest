from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from apps.anuncio.models import Anuncio
from apps.usuario.models import Usuario
from .serializers import AnuncioSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import CategoriaSerializer, AnuncioSerializer, OfertaAnuncioSerializer

class MisAnunciosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        anuncios = Anuncio.objects.filter(publicado_por=request.user)
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)

