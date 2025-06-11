from rest_framework import serializers
from ..models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'documento_identidad', 'domicilio']
