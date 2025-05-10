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

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        #actualizamos el user para encriptar la contraseña
        user = Usuario.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save() #sobrescribimos al usuario creado pero con contraseña encriptada
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user":serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(Usuario, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'error':"Contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user":serializer.data}, status=status.HTTP_200_OK)

class MisAnunciosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        anuncios = Anuncio.objects.filter(publicado_por=request.user)
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)
