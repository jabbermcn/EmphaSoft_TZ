import django_filters

from .models import Room


class RoomFilter(django_filters.FilterSet):
    capacity_min = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte',
    )
    capacity_max = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='lte',
    )
    price_min = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='gte',
    )
    price_max = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='lte',
    )

    class Meta:
        model = Room
        fields = []
