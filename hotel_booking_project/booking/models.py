from django.contrib.auth.models import User
from django.db import models

from room.models import Room


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking room number {self.room} by user:{self.user}'
