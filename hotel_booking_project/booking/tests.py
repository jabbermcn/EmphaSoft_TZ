from datetime import date
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from room.models import Room
from .models import Booking


class BookingViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_booking_success(self):
        room = Room.objects.create(name='Test Room', price_per_night=100, capacity=2)
        data = {
            'room': room.id,
            'check_in_date': '2023-01-01',
            'check_out_date': '2023-01-05',
        }

        with patch('booking.views.get_object_or_404') as mock_get_object_or_404:
            mock_get_object_or_404.return_value = room
            response = self.client.post('http://localhost:8000/api/bookings/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)

    def test_create_booking_invalid_request(self):
        data = {
            'check_in_date': '2023-01-01',
            'check_out_date': '2023-01-05',
        }

        response = self.client.post('http://localhost:8000/api/bookings/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_room_not_found(self):
        data = {
            'room': 999,
            'check_in_date': '2023-01-01',
            'check_out_date': '2023-01-05',
        }

        with patch('booking.views.get_object_or_404') as mock_get_object_or_404:
            mock_get_object_or_404.side_effect = Room.DoesNotExist
            response = self.client.post('http://localhost:8000/api/bookings/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_booking_room_not_available(self):
        room = Room.objects.create(name='Test Room', price_per_night=100, capacity=2)
        Booking.objects.create(
            user=self.user,
            room=room,
            check_in_date=date(2023, 1, 2),
            check_out_date=date(2023, 1, 4),
        )
        data = {
            'room': room.id,
            'check_in_date': '2023-01-01',
            'check_out_date': '2023-01-05',
        }

        with patch('booking.views.get_object_or_404') as mock_get_object_or_404:
            mock_get_object_or_404.return_value = room
            response = self.client.post('http://localhost:8000/api/bookings/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking_success(self):
        booking = Booking.objects.create(
            user=self.user,
            room=Room.objects.create(name='Test Room', price_per_night=100, capacity=2),
            check_in_date=date(2023, 1, 1),
            check_out_date=date(2023, 1, 5),
        )

        response = self.client.delete(f'http://localhost:8000/api/bookings/{booking.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Booking.objects.get(id=booking.id).is_cancelled)

    def test_cancel_booking_unauthorized(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        booking = Booking.objects.create(
            user=other_user,
            room=Room.objects.create(name='Test Room', price_per_night=100, capacity=2),
            check_in_date=date(2023, 1, 1),
            check_out_date=date(2023, 1, 5),
        )

        response = self.client.delete(f'http://localhost:8000/api/bookings/{booking.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Booking.objects.get(id=booking.id).is_cancelled)

    def test_get_user_bookings(self):
        room = Room.objects.create(name='Test Room', price_per_night=100, capacity=2)
        Booking.objects.create(
            user=self.user,
            room=room,
            check_in_date=date(2023, 1, 1),
            check_out_date=date(2023, 1, 5),
        )

        response = self.client.get('http://localhost:8000/api/bookings/user-bookings/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
