from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in_date', 'check_out_date', 'is_cancelled')
