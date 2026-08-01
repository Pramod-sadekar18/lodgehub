from django.urls import path
from .views import TripPlanRequestCreateAPIView

urlpatterns = [
    path('', TripPlanRequestCreateAPIView.as_view(), name='plan-trip-request'),
]
