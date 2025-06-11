import pytest
from apps.usuario.models import Usuario
from django.contrib.auth import get_user_model

@pytest.fixture
def test_password():
    return "secure_password_123"

@pytest.fixture
def create_user(test_password):
    def make_user(**kwargs):
        User = get_user_model()
        return User.objects.create_user(
            username=kwargs.get("username", "testuser"),
            password=test_password,
            documento_identidad=kwargs.get("documento_identidad", "123456789"),
            domicilio=kwargs.get("domicilio", "Calle Falsa 123"),
            email=kwargs.get("email", "test@example.com")
        )
    return make_user