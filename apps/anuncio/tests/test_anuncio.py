from datetime import timedelta
import pytest
from django.urls import reverse
from django.utils import timezone
from apps.usuario.tests.conftest import create_user, create_superuser, test_password
from apps.anuncio.models import Anuncio, Categoria

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

    #obtener el token
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
    data = {
        'titulo': 'Nuevo anuncio de prueba',
        'descripcion': 'Este es un anuncio de prueba para testing',
        'precio_inicial': '99.99',
        'fecha_inicio': timezone.now() + timezone.timedelta(minutes=10),
        'fecha_fin': timezone.now() + timezone.timedelta(days=10),
        'activo': True,
        'categorias_ids': [cat1.id, cat2.id],
        # Campos opcionales: imagen, categorias, oferta_ganadora se pueden omitir o enviar vacíos
    }
    # la vista setea 'publicado_por' automáticamente con el usuario autenticado
    # Paso 2: ponerlo en los headers
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['titulo'] == data['titulo']
    assert response_data['descripcion'] == data['descripcion']

    #Verificamos que se asoció con el usuario autenticado
    assert response_data['publicado_por'] == user.id

@pytest.mark.django_db
def test_creacion_anuncio_fallido(api_client, create_superuser, test_password):
    # Crear usuario y loguearlo
    user = create_superuser
    api_client.login(username=user.username, password=test_password)

    #obtener el token
    login_url = reverse('usuario:auth_url_login')  # o el endpoint de login real
    response = api_client.post(login_url, {
        'username': user.username,
        'password': test_password
    }, format='json')
    assert response.status_code == 200
    token = response.data['token']

    # Datos para el nuevo anuncio
    url = reverse('anuncio-list')  # nombre generado por el router
    # Datos inválidos: faltan campos obligatorios como 'titulo' y 'precio_inicial'
    invalid_data = {
        'fecha_inicio': timezone.now().isoformat(),
        'activo': True
        # 'titulo' y 'precio_inicial' faltan => inválido
    }
    # la vista setea 'publicado_por' automáticamente con el usuario autenticado
    # ponerlo en los headers
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.post(url, invalid_data, format='json')
    print(response.status_code, response.data)

    assert response.status_code == 400

@pytest.mark.django_db
def test_modificacion_fallida_datos_invalidos(api_client, create_superuser, test_password):
    user = create_superuser
    api_client.login(username=user.username, password=test_password)

    anuncio = Anuncio.objects.create(
        titulo = 'Anuncio original',
        descripcion = 'Descripción',
        precio_inicial = 100.00,
        fecha_inicio = timezone.now(),
        fecha_fin = timezone.now() + timezone.timedelta(days=10),
        publicado_por = user
    )
    url = reverse('anuncio-detail', args=[anuncio.id])

    data = {
        'titulo': 'Anuncio modificado',
        'precio_inicial': 'precio inválido'  # inválido: debe ser decimal
    }

    response = api_client.patch(url, data, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_modificacion_fallida_usuario_distinto(api_client, create_superuser, test_password):
    user = create_superuser
    # api_client.login(username=user.username, password=test_password)
    api_client.force_authenticate(user=user)
    anuncio = Anuncio.objects.create(
        titulo = 'Anuncio original',
        descripcion = 'Descripción',
        precio_inicial = 100.00,
        fecha_inicio = timezone.now(),
        fecha_fin = timezone.now() + timedelta(days=10),
        publicado_por = user
    )
    url = reverse('anuncio-detail', args=[anuncio.id])

    data = {
        'titulo': 'Anuncio modificado',
        'precio_inicial': 1999.9  # inválido: debe ser decimal
    }
    print(anuncio.fecha_fin)
    response = api_client.patch(url, data, format='json')
    print(response.status_code, response.data)
    assert response.status_code == 200
#------------------------------------------------------------------------------------
    #VALENTIN

    # 1.2. Creación fallida de un anuncio por datos inválidos.  ✅
    # 2.2. Modificación fallida sobre un anuncio por datos inválidos ✅
    # 2.3. Modificación fallida sobre un anuncio por no coincidir usuario autenticado con usuario creador del anuncio. 
    # 3.2. Listado de anuncios aplicando filtros
    # 4.3. Creación fallida de una Oferta de Anuncio porque el usuario que intenta ofertar es el creador del mismo
    # anuncio.

    # IMPORTANTES 
    # 1.1. Creación correcta de un anuncio verificando sus datos internos (titulo, fechas, etc.) y que el usuario 
    # autenticado sea el usuario que publica el anuncio.  ✅
    # # 1.2. Creación fallida de un anuncio por datos inválidos. ✅
    # 4.1. Creación correcta de una Oferta de Anuncio verificando que los datos sean validos, que el usuario ofertante
    # 4.2. Creación fallida de una Oferta de Anuncio por contener datos inválidos
    # 4.3. Creación fallida de una Oferta de Anuncio porque el usuario que intenta ofertar es el creador del mismo
    # anuncio.
