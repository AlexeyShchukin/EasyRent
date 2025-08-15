from django.contrib.auth import get_user_model
from django.db import models


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        REJECTED = 'Rejected', 'Rejected'
        CANCELLED = 'Cancelled', 'Cancelled'

    listing = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    renter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
