from rest_framework.views import exception_handler
import requests
from decimal import Decimal
from django.conf import settings

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 400:
        response.data = {
            "error": {
                "code": "400 Bad Request",
                "message": response.data
            }
        }
    return response


EXCHANGE_API_URL = 'https://v6.exchangerate-api.com/v6'
API_KEY = settings.EXCHANGE_RATE_API_KEY 

def convertir_precio(precio_ars, moneda_destino='USD'):
    try:
        response = requests.get(f'{EXCHANGE_API_URL}/{API_KEY}/latest/ARS')
        if response.status_code == 200:
            data = response.json()
            tasa = data['conversion_rates'].get(moneda_destino)
            if tasa:
                return round(Decimal(precio_ars) * Decimal(tasa), 2)
    except Exception as e:
        print(f"Error al convertir moneda: {e}")
    return None