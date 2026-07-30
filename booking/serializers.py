from rest_framework import serializers

from lodge.models import Room
from .models import Booking 
class BookingSerializer(serializers.ModelSerializer):

    available_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "room_name",
            "price_per_night",
            "capacity",
            "total_rooms",
            "available_rooms",
            "images"
        ]

    def get_available_rooms(self, obj):
        return obj.total_rooms

class MyBookingSerializer(serializers.ModelSerializer):

    property_name = serializers.CharField(
        source='property.name',
        read_only=True
    )

    class Meta:

        model = Booking

        fields = [
            'id',
            'property_name',
            'check_in',
            'check_out',
            'number_of_rooms',
            'total_price',
            'payment_status'
        ]