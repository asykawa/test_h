from django_filters import FilterSet, CharFilter
from .models import Property
import django_filters


class PropertyFilter(FilterSet):
    property_type = django_filters.ChoiceFilter(choices=Property.CONDITION_CHOICES)
    condition = django_filters.ChoiceFilter(choices=Property)

    class Meta:
        model = Property
        fields = {
            'region': ['exact'],
            'city': ['exact'],
            'area': ['gt', 'lt'],
            'property_type': ['exact'],
            'rooms': ['exact'],
            'floor': ['exact'],
            'condition': ['exact'],
            'image': ['exact'],
            'document': ['exact'],
            'price': ['gt', 'lt'],
            'district': ['exact'],
        }

class TypeFilter(FilterSet):
    # Фильтр по полю language_name из связанной модели Languages
    property_type = CharFilter(field_name='property_type__property_name', lookup_expr='exact')

    class Meta:
        model = Property
        fields = ['property_type']
