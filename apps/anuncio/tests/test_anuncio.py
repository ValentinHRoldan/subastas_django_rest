import pytest
from django.urls import reverse
from django.utils import timezone
from apps.usuario.tests.conftest import create_user, create_superuser, test_password
from apps.anuncio.models import Categoria

@pytest.mark.django_db
def test_anuncio_basico_titulo(anuncio_basico):
    assert anuncio_basico.titulo == 'Anuncio de prueba'
    assert anuncio_basico.descripcion == ''  # por defecto
    assert anuncio_basico.categorias.exists()  # opcional

@pytest.mark.django_db
def test_creacion_anuncio(api_client, create_superuser, test_password):
    # Crear usuario y loguearlo
    user = create_superuser
    api_client.login(username=user.username, password=test_password)

    # Paso 1: obtener el token
    login_url = reverse('usuario:auth_url_login')  # o el endpoint de login real
    response = api_client.post(login_url, {
        'username': user.username,
        'password': test_password
    }, format='json')
    assert response.status_code == 200
    token = response.data['token']

    cat1 = Categoria.objects.create(nombre='Categoría 1')
    cat2 = Categoria.objects.create(nombre='Categoría 2')


    # Datos para el nuevo anuncio
    url = reverse('anuncio-list')  # nombre generado por el router
    # data = {
    #     'titulo': 'Nuevo anuncio de prueba',
    #     'descripcion': 'Este es un anuncio de prueba para testing',
    #     'precio_inicial': '99.99',
    #     'fecha_inicio': timezone.now() + timezone.timedelta(minutes=10),
    #     'fecha_fin': timezone.now() + timezone.timedelta(days=10),
    #     'activo': True,
    #     'categorias_ids': [cat1.id, cat2.id],
    #     # Campos opcionales: imagen, categorias, oferta_ganadora se pueden omitir o enviar vacíos
    # }
    # Datos inválidos: faltan campos obligatorios como 'titulo' y 'precio_inicial'
    invalid_data = {
        'fecha_inicio': timezone.now().isoformat(),
        'activo': True
        # 'titulo' y 'precio_inicial' faltan => inválido
    }
    # Como la vista probablemente setea 'publicado_por' automáticamente con el usuario autenticado,
    # no lo enviamos en el payload
    # Paso 2: ponerlo en los headers
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.post(url, invalid_data, format='json')
    print(response.status_code, response.data)

    assert response.status_code == 400
    # response_data = response.json()
    # # assert response_data['titulo'] == invalid_data['titulo']
    # # assert response_data['descripcion'] == invalid_data['descripcion']

    # # Verificamos que se asoció con el usuario autenticado
    # assert response_data['publicado_por'] == user.id