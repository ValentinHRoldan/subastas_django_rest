from datetime import timedelta
import pytest
from django.urls import reverse
from django.utils import timezone
from apps.usuario.tests.conftest import create_user, create_superuser, test_password, grupo_usuarios_registrados
from apps.anuncio.models import Anuncio, Categoria
from rest_framework import status

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
def test_modificacion_fallida_usuario_distinto(api_client, create_superuser, test_password, crear_anuncio, create_user, grupo_usuarios_registrados):
    user = create_superuser
    usuarioIntruso = create_user 
    cat1 = Categoria.objects.create(nombre='Categoría 1')
    cat2 = Categoria.objects.create(nombre='Categoría 2')
    anuncio = crear_anuncio(publicado_por=user, categorias=[cat1.id, cat2.id])
    
    api_client.force_authenticate(user=usuarioIntruso)

    url = reverse('anuncio-detail', args=[anuncio.id])

    data = {
        'titulo': 'Otro titulo',
    }
    response = api_client.patch(url, data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
def test_listado_anuncios_filtros(api_client, create_user, test_password, grupo_usuarios_registrados):
    user = create_user
    api_client.force_authenticate(user=user)

    params = {
        'activo': '',
        'ordering': '-titulo'
    }

    url = reverse('anuncio-list')
    response = api_client.get(url, params, format='json')
    assert response.status_code == 200

from django.core.exceptions import ValidationError
from decimal import Decimal
from apps.anuncio.models import OfertaAnuncio

@pytest.mark.django_db
def test_oferta_fallida_por_ser_el_creador(api_client, create_user, crear_anuncio, test_password, grupo_usuarios_registrados):
    user = create_user
    
    categoria = Categoria.objects.create(nombre="Electrónica")
    anuncio = crear_anuncio(publicado_por=user, categorias=[categoria.id])

    api_client.force_authenticate(user=user)
    # Intentamos crear una oferta con el mismo usuario
    data = {
        "precio_oferta": "200.00"
    }

    url = reverse("anuncio-ofertar", args=[anuncio.id])  # usa el nombre de la acción

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
#------------------------------------------------------------------------------------
    #VALENTIN

    # 1.2. Creación fallida de un anuncio por datos inválidos.  ✅
    # 2.2. Modificación fallida sobre un anuncio por datos inválidos ✅
    # 2.3. Modificación fallida sobre un anuncio por no coincidir usuario autenticado con usuario creador del anuncio. ✅
    # 3.2. Listado de anuncios aplicando filtros ✅
    # reverse('anuncio-detail', kwargs={'pk': anuncio.id})
    # 4.3. Creación fallida de una Oferta de Anuncio porque el usuario que intenta ofertar es el creador del mismo
    # anuncio.
# {
# "username": "valentin",
# "password": 11111
# }
# http://127.0.0.1:8000/api/anuncio/?activo=&ordering=-titulo
    # IMPORTANTES 
    # 1.1. Creación correcta de un anuncio verificando sus datos internos (titulo, fechas, etc.) y que el usuario 
    # autenticado sea el usuario que publica el anuncio.  ✅
    # # 1.2. Creación fallida de un anuncio por datos inválidos. ✅
    # 4.1. Creación correcta de una Oferta de Anuncio verificando que los datos sean validos, que el usuario ofertante
    # 4.2. Creación fallida de una Oferta de Anuncio por contener datos inválidos
    # 4.3. Creación fallida de una Oferta de Anuncio porque el usuario que intenta ofertar es el creador del mismo
    # anuncio.
