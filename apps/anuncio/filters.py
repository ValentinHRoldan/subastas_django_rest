from django_filters import rest_framework as filters
from apps.anuncio.models import Categoria

class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    
class Meta:
    model = Categoria
    fields = ['nombre', 'activa']
