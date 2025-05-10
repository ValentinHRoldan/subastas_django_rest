from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer
# Create your views here.
@api_view(['GET'])
def perfil(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }, status=status.HTTP_200_OK)
