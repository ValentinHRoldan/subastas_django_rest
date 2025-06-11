import pytest
from django.urls import reverse
from apps.usuario.models import Usuario

@pytest.mark.django_db
def test_login_usuario(client, create_user, test_password):
    user = create_user
    url = reverse('usuario:auth_url_login')

    response = client.post(url, {
        'username': user.username,
        'password': test_password
    })
    assert response.status_code == 200

@pytest.mark.django_db
def test_registro_usuario(client):
    url = reverse('usuario:auth_url_register')
    datos_usuario = {
        'username': 'nuevo_usuario',
        'password': 'passwordseguro123',
        'documento_identidad': '1234567890',
        'domicilio': 'Calle falsa 123'
    }
    response = client.post(url, datos_usuario)
    assert response.status_code == 201
    # se verifica si el usuario creado existe 
    assert Usuario.objects.filter(username='nuevo_usuario').exists()

    # Verifica contenido de la respuesta
    # Por ejemplo, que contenga el ID del nuevo usuario o un token de autenticación
    data = response.json()
    assert 'id' in data or 'token' in data