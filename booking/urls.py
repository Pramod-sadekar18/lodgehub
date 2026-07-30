from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, booking_page
from accounts.views import MyBookingsAPIView


router = DefaultRouter()

router.register(
    r'bookings',
    BookingViewSet,
    basename='booking'
)


urlpatterns = [

    path(
        "booking/<int:property_id>/",
        booking_page,
        name="booking-page"
    ),

    path(
        "my-bookings/",
        MyBookingsAPIView.as_view(),
        name="my_bookings"
    ),

    path(
        "",
        include(router.urls)
    ),
]