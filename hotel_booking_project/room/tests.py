from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from booking.models import Booking
from .models import Room
from .filters import RoomFilter


class RoomFilterTests(TestCase):
    def setUp(self):
        self.room1 = Room.objects.create(name='test1', capacity=2, price_per_night=100)
        self.room2 = Room.objects.create(name='test2', capacity=4, price_per_night=150)

    def test_capacity_range_filter(self):
        filter = RoomFilter(data={'capacity_range': '2:4'})
        filtered_rooms = filter.qs
        self.assertEqual(filtered_rooms.count(), 2)
        self.assertIn(self.room1, filtered_rooms)
        self.assertIn(self.room2, filtered_rooms)

    # def test_invalid_capacity_range(self):
    #     filter = RoomFilter(data={'capacity_range': '4:2'})
    #     with self.assertRaises(ValidationError) as error:
    #         filter.qs
    #     self.assertEqual(
    #         str(error.exception),
    #         "Validation error(s): {'range':['Capacity min cannot be greater than capacity max.']}"
    #     )

    def test_price_range_filter(self):
        filter = RoomFilter(data={'price_range': '100:150'})
        filtered_rooms = filter.qs
        self.assertEqual(filtered_rooms.count(), 2)
        self.assertIn(self.room1, filtered_rooms)
        self.assertIn(self.room2, filtered_rooms)

    # def test_invalid_price_range(self):
    #     filter = RoomFilter(data={'price_range': '150:100'})
    #     with self.assertRaises(ValidationError) as error:
    #         filter.qs
    #     self.assertEqual(
    #         str(error.exception),
    #         "Validation error(s): {'range':['Price min cannot be greater than price max.']}"
    #     )

    def test_available_dates_filter(self):
        user = User.objects.create(username='test_user', password='password')
        booking1 = Booking.objects.create(room=self.room1, user=user, check_in_date=date(2023, 12, 16),
                                          check_out_date=date(2023, 12, 18))
        booking2 = Booking.objects.create(room=self.room2, user=user, check_in_date=date(2023, 12, 20),
                                          check_out_date=date(2023, 12, 22))

        filter = RoomFilter(data={'available': '2023-12-17:2023-12-19'})
        filtered_rooms = filter.qs
        self.assertEqual(filtered_rooms.count(), 2)
        self.assertIn(self.room2, filtered_rooms)

    # def test_invalid_single_date(self):
    #     filter = RoomFilter(data={'available': '2023-12-18'})
    #     with self.assertRaises(ValidationError) as error:
    #         filter.qs
    #     self.assertEqual(
    #         str(error.exception),
    #         "Validation error(s): {'detail': 'available_before and available_after has to be specified.'}"
    #     )

    # def test_invalid_same_dates(self):
    #     filter = RoomFilter(data={'available': '2023-12-18:2023-12-18'})
    #     with self.assertRaises(ValidationError) as error:
    #         filter.qs
    #     self.assertEqual(
    #         str(error.exception),
    #         "Validation error(s): {'detail': 'available_before and available_after has to differ.'}"
    #     )
