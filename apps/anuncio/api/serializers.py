from rest_framework import serializers
from ..models import Categoria, Anuncio, OfertaAnuncio
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.usuario.models import Usuario

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
        ] 
    # def create(self, validated_data):
    #     categorias_data = validated_data.pop('categorias')
    #     anuncio = Anuncio.objects.create(**validated_data)
    #     for categoria_data in categorias_data:
    #         categoria_id = categoria_data.get('id') # Obtiene el id si está presente
    #         if categoria_id:
    #             try:
    #                 categoria = Categoria.objects.get(id=categoria_id)
    #             except Categoria.DoesNotExist:
    #                 categoria = Categoria.objects.create(**categoria_data)
    #         else:
    #             categoria = Categoria.objects.create(**categoria_data)
    #         if categoria: # Si la categoría existe o se creó, la añade al anuncio
    #             anuncio.categorias.add(categoria)
    #     return anuncio

class AnuncioSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    categorias_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Categoria.objects.all(), write_only=True
    )

    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',      
            'categorias_ids',  
            'publicado_por',
            'oferta_ganadora',
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']

    def create(self, validated_data):
        categorias = validated_data.pop('categorias_ids', [])
        anuncio = Anuncio.objects.create(**validated_data)
        anuncio.categorias.set(categorias)
        return anuncio
    
    # def generarError(self, mensaje):
    #     raise serializers.ValidationError({
    #         'info': mensaje
    #     })

    # def validate_fecha_inicio(self, value):
    #     if value < timezone.now():
    #         self.generarError('la fecha no puede ser anterior a la actual')
    #     return value
    
    def errorMessage(self, info):
        return {
            'info': info
        }

    def validate(self,data):
        errors = {}
        fecha_maxima = timezone.now() + timedelta(days=30) # fecha maxima establecida a 30 dias
        duracion = data['fecha_fin'] - data['fecha_inicio']
        duracion_maxima = timedelta(days=30 * 2)
        if data['fecha_inicio'] < timezone.now():
            errors['fecha_inicio'] = self.errorMessage('La fecha no puede ser anterior a la actual.')

        if data['fecha_fin'] < data['fecha_inicio']:
            errors['fecha_fin'] = self.errorMessage('La fecha no puede ser anterior a la fecha de inicio')

        if data['fecha_inicio'] > fecha_maxima:
            errors['fecha_fin'] = self.errorMessage('La fecha de inicio no puede ser mayor a 30 dias desde ahora')

        if duracion > duracion_maxima:
            errors['Subasta'] = self.errorMessage('La duracion de la subasta no debe superar los 60 dias')
            
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'documento_identidad', 'domicilio']

class OfertaAnuncioSerializer(serializers.ModelSerializer):
    anuncio = AnuncioSerializer(many=False, read_only=True)

    class Meta:
        model = OfertaAnuncio
        fields = [
            'anuncio',
            'fecha_oferta',
            'precio_oferta',
            'usuario'
        ]
        read_only_fields = ['usuario', 'anuncio', 'es_ganador']
    
