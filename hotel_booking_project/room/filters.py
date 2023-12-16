import django_filters
from django.db.models import QuerySet, Q
from django_filters.widgets import RangeWidget
from rest_framework.exceptions import ValidationError

from .models import Room


class MyRangeWidget(django_filters.widgets.RangeWidget):

    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class RoomFilter(django_filters.FilterSet):
    capacity_range = django_filters.RangeFilter(
        field_name='capacity',
        lookup_expr='gte__lte',
        widget=MyRangeWidget(
            from_attrs={
                'placeholder': 'capacity - min',
            },
            to_attrs={
                'placeholder': 'capacity - max',
            },
        )
    )
    price_range = django_filters.RangeFilter(
        field_name='price_per_night',
        lookup_expr='gte__lte',
        widget=MyRangeWidget(
            from_attrs={
                'placeholder': 'price_per_night - min',
            },
            to_attrs={
                'placeholder': 'price_per_night - max',
            },
        )
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
            bookings__check_in_date__lt=value.stop,
            bookings__check_out_date__gt=value.start,
            booking__is_cancelled=False,
        )

        return queryset
