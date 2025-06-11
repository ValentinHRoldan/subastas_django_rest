import pytest
from apps.usuario.models import Usuario
from django.contrib.auth import get_user_model

@pytest.fixture
def test_password():
    return "secure_password_123"

@pytest.fixture
def create_user(test_password):
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        password=test_password,
        documento_identidad="123456789",
        domicilio="Calle Falsa 123",
        email="test@example.com",
    )
    return user


@pytest.fixture
def create_superuser(test_password):
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        password=test_password,
        documento_identidad="123456789",
        domicilio="Calle Falsa 123",
        email="test@example.com",
        is_superuser = True
    )
    return user