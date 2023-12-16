from datetime import datetime
from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from room.models import Room
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):

    """
    API endpoint for managing bookings.

    create:
    Create a new booking.

    destroy:
    Cancel a booking.

    get_user_bookings:
    Get a list of bookings for the authenticated user.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new booking.
        """
        room_id: int | None = request.data.get('room')
        check_in_str: str | None = request.data.get('check_in_date')
        check_out_str: str | None = request.data.get('check_out_date')

        if not (room_id and check_in_str and check_out_str):
            return Response({'message': 'Invalid request. Make sure all required fields are provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()

            room: Room = get_object_or_404(Room, pk=room_id)

            existing_bookings: list[Booking] = Booking.objects.filter(room=room)
            for booking in existing_bookings:
                if check_in_date <= booking.check_out_date and check_out_date >= booking.check_in_date:
                    return Response({'message': 'Room not available for the selected dates.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            booking: Booking = Booking.objects.create(
                user=request.user,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                is_cancelled=False,
            )
            return Response({'message': 'Room reserved successfully.'}, status=status.HTTP_201_CREATED)

        except Room.DoesNotExist:
            return Response({'message': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Cancel a booking.
        """
        booking = self.get_object()
        if booking.user == request.user:
            booking.is_cancelled = True
            booking.save()
            return Response({'message': 'Reservation canceled'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to cancel this reservation.'},
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='user-bookings')
    def get_user_bookings(self, request: Request) -> Response:
        """
        Get a list of bookings for the authenticated user.
        """
        bookings = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


