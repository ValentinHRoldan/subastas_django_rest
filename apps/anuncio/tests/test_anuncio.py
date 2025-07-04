from datetime import timedelta
import pytest
from django.urls import reverse
from django.utils import timezone
from apps.usuario.tests.conftest import create_user, create_superuser, test_password, grupo_usuarios_registrados
from apps.anuncio.models import Anuncio, Categoria, OfertaAnuncio
from rest_framework import status
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from .fixtures_categoria import get_categoria
from .fixtures_anuncio import get_anuncio, get_user_generico_anuncio

@pytest.mark.django_db
def test_creacion_anuncio(api_client, create_superuser, test_password):
    # Crear usuario y logueo
    user = create_superuser
    api_client.login(username=user.username, password=test_password)

    #token
    login_url = reverse('usuario:auth_url_login')
    response = api_client.post(login_url, {
        'username': user.username,
        'password': test_password
    }, format='json')
    assert response.status_code == 200
    token = response.data['token']

    cat1 = Categoria.objects.create(nombre='Categoría 1')
    cat2 = Categoria.objects.create(nombre='Categoría 2')

    url = reverse('anuncio-list')  # nombre generado por el router
    data = {
        'titulo': 'Nuevo anuncio de prueba',
        'descripcion': 'Este es un anuncio de prueba para testing',
        'precio_inicial': 99.99,
        'fecha_inicio': timezone.now() + timezone.timedelta(minutes=10),
        'fecha_fin': timezone.now() + timezone.timedelta(days=10),
        'activo': True,
        'categorias_ids': [cat1.id, cat2.id],
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['titulo'] == data['titulo']
    assert response_data['descripcion'] == data['descripcion']

    assert response_data['publicado_por'] == user.id

@pytest.mark.django_db
def test_creacion_anuncio_fallido(api_client, create_superuser, test_password):
    user = create_superuser
    api_client.login(username=user.username, password=test_password)

    #token
    login_url = reverse('usuario:auth_url_login')  # o el endpoint de login real
    response = api_client.post(login_url, {
        'username': user.username,
        'password': test_password
    }, format='json')
    assert response.status_code == 200
    token = response.data['token']

    url = reverse('anuncio-list')
    invalid_data = {
        'fecha_inicio': timezone.now().isoformat(),
        'activo': True
        # 'titulo' y 'precio_inicial' faltan => inválido
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.post(url, invalid_data, format='json')

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
        'precio_inicial': 'precio invalido' 
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
        'ordering': '-titulo'
    }

    url = reverse('anuncio-list')
    response = api_client.get(url, params, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_oferta_fallida_por_ser_el_creador(api_client, create_user, crear_anuncio, test_password, grupo_usuarios_registrados):
    user = create_user
    
    categoria = Categoria.objects.create(nombre="Electrónica")
    anuncio = crear_anuncio(publicado_por=user, categorias=[categoria.id])

    api_client.force_authenticate(user=user)

    data = {
        "precio_oferta": "200.00"
    }

    url = reverse("anuncio-ofertar", args=[anuncio.id]) 

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
    # anuncio. ✅
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
    # 4.3. Creación fallida de una Oferta de Anuncio porque el usuario que intenta ofertar es el creador del mismo ✅
    # anuncio.


def test_foo():
    assert True


def test_lista():
    assert list(reversed([1, 2, 3])) == [3, 2, 1]

@pytest.mark.django_db
def test_api_creacion_anuncio(get_authenticated_client): #1.1
    client = get_authenticated_client

    data = {
        "nombre": "Equipo deportivo",
    }

    response = client.post(f'/api/categoria/', data=data)

    data = {
        "titulo": "par de mancuernas",
        "descripcion": "de 5kg c/u",
        "precio_inicial": "30000",
        "fecha_inicio": "2025-06-15",
        "fecha_fin": "2025-06-30",
        "categorias_ids": [
            1
        ]
    }
    print(client._credentials)
    response = client.post(f'/api/anuncio/', data=data)
    assert response.status_code == 201
    assert Anuncio.objects.filter(titulo='par de mancuernas').count() == 1

@pytest.mark.django_db
def test_api_mod_anuncio(get_authenticated_client,get_categoria): #2.1

    client = get_authenticated_client

    data = {
        "titulo": "par de mancuernas",
        "descripcion": "de 5kg c/u",
        "precio_inicial": "30000",
        "fecha_inicio": "2025-06-15",
        "fecha_fin": "2025-06-30",
        "categorias_ids": [
            1
        ]
    }

    response = client.post(f'/api/anuncio/', data=data)

    data = {
        "descripcion": "de 5.5kg c/u",
        "precio_inicial": "32000",
    }
    print(client._credentials)
    response = client.patch(f'/api/anuncio/1/', data=data)
    assert response.status_code == 200
    assert Anuncio.objects.filter(titulo='par de mancuernas').count() == 1

@pytest.mark.django_db
def test_api_lista_anuncios(get_authenticated_client, get_anuncio): #3.1
    cliente = get_authenticated_client

    anuncio = get_anuncio

    response = cliente.get(f'/api/anuncio/')
    assert response.status_code == 200

    data = response.data
    assert data[0]['titulo'] == anuncio.titulo

@pytest.mark.django_db
def test_api_creacion_oferta_anuncio(get_authenticated_client, get_categoria, get_anuncio): #4.1
    client = get_authenticated_client

    data = {
        "precio_oferta": "150001"
    }

    response = client.post(f'/api/anuncio/1/ofertar/', data=data)
    assert response.status_code == 201
    assert OfertaAnuncio.objects.filter(precio_oferta='150001',anuncio=get_anuncio).count() == 1


@pytest.mark.django_db
def test_api_fallo_creacion_oferta_anuncio_datos_invalidos(get_authenticated_client, get_categoria, get_anuncio): #4.2
    client = get_authenticated_client

    data = {
        "precio_oferta": "149999.99"
    }

    response = client.post(f'/api/anuncio/1/ofertar/', data=data)
