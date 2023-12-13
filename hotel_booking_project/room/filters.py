from datetime import date

import django_filters

from .models import Room


class RoomFilter(django_filters.FilterSet):
    capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte',
    )
    max_price = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='lte',
    )
    check_in_date = django_filters.DateFilter(
        method='filter_rooms_for_check_in',
    )
    check_out_date = django_filters.DateFilter(
        method='filter_rooms_for_check_out',
    )

    class Meta:
        model = Room
        fields = ['capacity', 'price_per_night']

    def filter_rooms_for_check_in(self, queryset, name: str, check_in_date: date) -> Room:
        """
        Filter for available rooms during the specified check-in date.
        """
        return queryset.exclude(booking__check_out_date__gte=check_in_date, booking__check_in_date__lte=check_in_date)

    def filter_rooms_for_check_out(self, queryset, name: str, check_out_date: date) -> Room:
        """
        Filter for available rooms during the specified check-out date.
        """
        return queryset.exclude(booking__check_out_date__gte=check_out_date, booking__check_in_date__lte=check_out_date)
