import django_filters
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from .models import Room


class RoomFilter(django_filters.FilterSet):
    capacity_range = django_filters.RangeFilter(
        field_name='capacity',
        lookup_expr='gte__lte',
    )
    price_range = django_filters.RangeFilter(
        field_name='price_per_night',
        lookup_expr='gte__lte',
    )
    available = django_filters.DateFromToRangeFilter(
        method='available_filter',
        label='Available dates',
    )

    class Meta:
        model = Room
        fields = ['capacity_range', 'price_range']

    def available_filter(self, queryset, name, value: slice) -> QuerySet:
        if not (value.start and value.stop):
            raise ValidationError(
                {'detail': 'available_before and available_after has to be specified.'}
            )

        if value.start.date() == value.stop.date():
            raise ValidationError(
                {'detail': 'available_before and available_after has to differ.'}
            )

        queryset = queryset.exclude(
            booking__check_in_date__lt=value.stop,
            booking__check_out_date__gt=value.start,
        )
        return queryset
