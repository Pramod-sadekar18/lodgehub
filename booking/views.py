from django.shortcuts import render

# Create your views here.
from datetime import datetime
from django.db.models import Sum
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Booking, Room
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        room_id = request.data.get("room")
        property_id = request.data.get("property")

        check_in = datetime.strptime(
            request.data.get("check_in"),
            "%Y-%m-%d"
        ).date()

        check_out = datetime.strptime(
            request.data.get("check_out"),
            "%Y-%m-%d"
        ).date()

        number_of_rooms = int(
            request.data.get("number_of_rooms")
        )

        guests = int(
            request.data.get("guests")
        )

        guest_type = request.data.get("guest_type")

        room = Room.objects.get(id=room_id)

        # Calculate already booked rooms
        booked = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).aggregate(
            total=Sum("number_of_rooms")
        )

        booked_rooms = booked["total"] or 0

        available_rooms = room.total_rooms - booked_rooms

        if number_of_rooms > available_rooms:

            return Response(
                {
                    "message": "Rooms not available",
                    "available_rooms": available_rooms
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        nights = (check_out - check_in).days

        total_price = (
            room.price_per_night *
            nights *
            number_of_rooms
        )

        booking = Booking.objects.create(

            user=request.user,

            property_id=property_id,

            room=room,

            check_in=check_in,

            check_out=check_out,

            guests=guests,

            guest_type=guest_type,

            number_of_rooms=number_of_rooms,

            total_price=total_price
        )

        serializer = BookingSerializer(booking)

        if check_out <= check_in:
            return Response(
                {"message": "Check-out date must be after check-in date."},
                status=status.HTTP_400_BAD_REQUEST
            )
        


from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def booking_page(request, property_id):

    return render(
        request,
        "booking.html",
        {
            "property_id": property_id
        }
    )