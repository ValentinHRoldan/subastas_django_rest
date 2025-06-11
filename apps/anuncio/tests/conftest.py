import pytest
from apps.anuncio.models import Anuncio, Categoria
from apps.usuario.models import Usuario
from django.utils import timezone
from datetime import timedelta

@pytest.fixture
def usuario():
    return Usuario.objects.create_user(
        username='testuser',
        password='testpass',
        documento_identidad='11111111'
    )

@pytest.fixture
def categoria():
    return Categoria.objects.create(nombre='Electrónica')

@pytest.fixture
def anuncio_basico(usuario, categoria):
    anuncio = Anuncio.objects.create(
        titulo='Anuncio de prueba',
        precio_inicial=100.00,
        publicado_por=usuario
    )
    anuncio.categorias.add(categoria)
    return anuncio

@pytest.fixture
def crear_anuncio():
    def make_anuncio(publicado_por, categorias=None, **kwargs):
        anuncio = Anuncio.objects.create(
            titulo=kwargs.get('titulo', 'Anuncio original'),
            descripcion=kwargs.get('descripcion', 'Descripción'),
            precio_inicial=kwargs.get('precio_inicial', 100.00),
            fecha_inicio=kwargs.get('fecha_inicio', timezone.now()),
            fecha_fin=kwargs.get('fecha_fin', timezone.now() + timedelta(days=10)),
            publicado_por=publicado_por
        )
        if categorias:
            anuncio.categorias.set(categorias)
        return anuncio
    return make_anuncio

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()




