from django.contrib import admin
from django.urls import path 
from .views import RegisterView ,register_page ,LoginAPIView ,login_ui,ProfileAPIView ,home_page, payment_page ,profile_page,MyBookingSerializer
from booking.views import booking_page
from accounts import views


urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("register_ui/",register_page,name="register_page"),
    path('login/',LoginAPIView.as_view(), name='login'),
    path("login_ui/",views.login_ui, name="login_ui"),
    #path("profile/",ProfileAPIView.as_view(),name="profile"),
    path("payment/",payment_page,name="payment"),
    path("",views.home_page,name="home"),
    path('profile/',profile_page, name='profile_page'
),

]