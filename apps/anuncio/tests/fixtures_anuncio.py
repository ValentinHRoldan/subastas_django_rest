import pytest
from apps.anuncio.models import Anuncio, Categoria
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def get_anuncio(get_user_generico_anuncio):

    usuario = get_user_generico_anuncio

    categoria, _ = Categoria.objects.get_or_create(nombre='Deportes')

    anuncio, created= Anuncio.objects.get_or_create(
        titulo='Bicicleta',
        publicado_por=usuario,
        defaults={

            "descripcion": "Bicicleta de montaña en buen estado.",
            "precio_inicial": "150000",
            "fecha_inicio": "2025-06-16",
            "fecha_fin": "2025-06-30",
        }
    )
    if created:
        anuncio.categorias.add(categoria)

    return anuncio

def create_user(username, documento_identidad, first_name='usuario', last_name='prueba', password='unpassword', email=None, *, is_active=True):
    email = '{}@root.com'.format(username) if email is None else email

    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        user.documento_identidad = documento_identidad
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        user.set_password(password)  # Se Hashea la contraseña al guardarla en la BD
        user.save()

    return user

@pytest.fixture
def get_user_generico_anuncio():
    test_user = create_user(username='test2', documento_identidad='44326598', first_name='usuario', last_name='last_name', email='test@user.com')
    return test_user
