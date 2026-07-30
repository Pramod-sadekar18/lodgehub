from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView 
from .serializer import RegisterSerializer ,LoginSerializer

class RegisterView (CreateAPIView):
    serializer_class = RegisterSerializer 

# accounts/views.py

from django.shortcuts import render

def register_page(request):
    return render(request,'register.html')



# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

def login_ui(request):
    return render (request,"login.html")

def home_page(request):
    return render (request,"home.html")


def payment_page(request):
    return render(request, "payment.html")


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import  APIView


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name
        })

from booking.serializers import MyBookingSerializer
from booking.models import Booking
class MyBookingsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        bookings = Booking.objects.filter(
            user=request.user
        ).order_by("-booked_at")

        serializer = MyBookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)
        

def profile_page(request):
    return render(request, "profile.html")