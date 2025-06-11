from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.usuario',
    'apps.anuncio',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'drf_spectacular'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

AUTH_USER_MODEL = 'usuario.Usuario'

ROOT_URLCONF = 'subastas_clase.urls'

import environ

# Inicializa django-environ
env = environ.Env()
environ.Env.read_env()  # Lee las variables del archivo .env

# Usa la variable EXCHANGE_RATE_API_KEY desde el archivo .env
EXCHANGE_RATE_API_KEY = env('EXCHANGE_RATE_API_KEY')

SECRET_KEY = 'django-insecure-ogj^q#mk!a9y20w9yh$&ch2xz($n_aprls6-czdvus0hgfbri2'