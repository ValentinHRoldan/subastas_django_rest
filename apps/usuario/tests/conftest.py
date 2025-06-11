import pytest
from apps.usuario.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.anuncio.models import Anuncio

@pytest.fixture
def test_password():
    return "secure_password_123"

@pytest.fixture
def grupo_usuarios_registrados():
    group, created = Group.objects.get_or_create(name="usuarios_registrados")

    content_type = ContentType.objects.get_for_model(Anuncio)
    permisos = Permission.objects.filter(
        content_type=content_type,
        codename__in=[
            'view_anuncio',
            'add_anuncio',
            'change_anuncio',
            'delete_anuncio',
        ]
    )
    group.permissions.set(permisos)
    return group


@pytest.fixture
def create_user(test_password, grupo_usuarios_registrados):
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        password=test_password,
        documento_identidad="12345678",
        domicilio="Calle Falsa 123",
        email="test@example.com",
    )
    user.groups.add(grupo_usuarios_registrados)
    return user


@pytest.fixture
def create_superuser(test_password):
    User = get_user_model()
    user = User.objects.create_user(
        username="testsuperuser",
        password=test_password,
        documento_identidad="87654321",
        domicilio="Calle Falsa 123",
        email="testsup@example.com",
        is_superuser = True
    )
    return user