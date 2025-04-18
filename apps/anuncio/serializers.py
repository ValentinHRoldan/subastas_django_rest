from rest_framework import serializers
from .models import Categoria, Anuncio

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