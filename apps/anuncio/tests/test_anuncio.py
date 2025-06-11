import pytest
from django.urls import reverse
from apps.usuario.models import Usuario

@pytest.mark.django_db
def test_anuncio_basico_titulo(anuncio_basico):
    assert anuncio_basico.titulo == 'Anuncio de prueba'
    assert anuncio_basico.descripcion == ''  # por defecto
    assert anuncio_basico.categorias.exists()  # opcional
