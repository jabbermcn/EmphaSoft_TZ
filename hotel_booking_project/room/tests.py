from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from booking.models import Booking
from .models import Room
from .filters import RoomFilter


class RoomFilterTest(TestCase):
    def setUp(self):
        # Create a user for bookings
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data for rooms and bookings
        self.room1 = Room.objects.create(name='Test room 1', capacity=2, price_per_night=100)
        self.room2 = Room.objects.create(name='Test room 2', capacity=4, price_per_night=150)
        self.room3 = Room.objects.create(name='Test room 3', capacity=3, price_per_night=120)

        # Create bookings for the rooms
        Booking.objects.create(room=self.room1, user=self.user, check_in_date=date(2023, 1, 1),
                               check_out_date=date(2023, 1, 5))
        Booking.objects.create(room=self.room2, user=self.user, check_in_date=date(2023, 2, 1),
                               check_out_date=date(2023, 2, 5))

    def test_filter_rooms_for_check_in(self):
        # Filter rooms available on January 3, 2023
        check_in_date = date(2023, 1, 3)
        filtered_rooms = RoomFilter(data={'check_in_date': check_in_date}).qs

        # Only room3 should be available on January 3, 2023
        self.assertQuerysetEqual(filtered_rooms, [self.room3], transform=lambda x: x)

    def test_filter_rooms_for_check_out(self):
        # Filter rooms available on February 3, 2023
        check_out_date = date(2023, 2, 3)
        filtered_rooms = RoomFilter(data={'check_out_date': check_out_date}).qs

        # Only room1 should be available on February 3, 2023
        self.assertQuerysetEqual(filtered_rooms, [self.room1], transform=lambda x: x)
