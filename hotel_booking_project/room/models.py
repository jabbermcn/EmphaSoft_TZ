from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=10)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
