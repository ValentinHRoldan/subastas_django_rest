import pytest

from apps.anuncio.models import Categoria


@pytest.fixture
def get_categoria():
    categoria, _ = Categoria.objects.get_or_create(
        nombre='Muebles',
        defaults={
            "activa": True
        }
    )

    return categoria


@pytest.fixture
def get_categorias():
    categoria1, _ = Categoria.objects.get_or_create(
        nombre='Computacion',
        defaults={
            "activa": True
        }
    )
    categoria2, _ = Categoria.objects.get_or_create(
        nombre='Electronica',
        defaults={
            "activa": True
        }
    )
    categoria3, _ = Categoria.objects.get_or_create(
        nombre='Hogar',
        defaults={
            "activa": False
        }
    )

    return categoria1, categoria2, categoria3
