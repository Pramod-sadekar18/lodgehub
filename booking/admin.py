from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "property",
        "room",
        "check_in",
        "check_out",
        "number_of_rooms",
        "guests",
        "guest_type",
        "total_price",
        "payment_status",
        "booking_status",
    )

    list_filter = (
        "guest_type",
        "payment_status",
        "booking_status",
        "check_in",
        "check_out",
    )

    search_fields = (
        "user__username",
        "property__name",
        "room__room_name",
    )

    ordering = ("-booked_at",)

    readonly_fields = (
        "total_price",
        "booked_at",
    )