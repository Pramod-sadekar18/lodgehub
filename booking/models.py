

# Create your models here.
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from lodge.models import Property,Room 

class Booking(models.Model):

    GUEST_TYPE_CHOICES = [
        ('family', 'Family'),
        ('gents', 'Only Gents'),
        ('ladies', 'Only Ladies'),
        ('couple', 'Couple'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    BOOKING_STATUS = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.PositiveIntegerField()

    number_of_rooms = models.PositiveIntegerField(default=1)

    guest_type = models.CharField(
        max_length=20,
        choices=GUEST_TYPE_CHOICES
    )

    def clean(self):

        if self.number_of_rooms > self.room.total_rooms:
            raise ValidationError(
                f"Only {self.room.total_rooms} room(s) available."
            )

        if self.check_out <= self.check_in:
            raise ValidationError(
                "Check-out date must be after check-in date."
            )


    def save(self, *args, **kwargs):

        # Run model validation
        self.full_clean()

        nights = (self.check_out - self.check_in).days

        self.total_price = (
            self.room.price_per_night
            * nights
            * self.number_of_rooms
        )

        super().save(*args, **kwargs)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='booked'
    )

    payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.room_name}"