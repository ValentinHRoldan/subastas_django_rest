import pytest
from apps.anuncio.models import Anuncio, Categoria
from apps.usuario.models import Usuario

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
def api_client():
    from rest_framework.test import APIClient
    return APIClient()




