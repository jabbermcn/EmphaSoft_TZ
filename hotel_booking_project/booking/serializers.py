from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'is_cancelled')
        read_only_fields = ('user',)
