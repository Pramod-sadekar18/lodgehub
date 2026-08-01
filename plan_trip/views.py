from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import TripPlanRequest
from .serializers import TripPlanRequestSerializer


class TripPlanRequestCreateAPIView(CreateAPIView):
    queryset = TripPlanRequest.objects.all()
    serializer_class = TripPlanRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Thank you! We have received your trip request. A travel expert will contact you shortly.',
                'request': serializer.data,
            }
        )
