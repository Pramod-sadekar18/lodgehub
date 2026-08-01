from django.urls import path
from .views import plan_trip_page, plan_trip_success_page

urlpatterns = [
    path("", plan_trip_page, name="plan_trip_form"),
    path("success/", plan_trip_success_page, name="plan_trip_success"),
]
