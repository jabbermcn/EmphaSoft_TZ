from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import RoomFilter
from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing rooms.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = RoomFilter
    ordering_fields = ['price_per_night', 'capacity']
    ordering = ['name']


