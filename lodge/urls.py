from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet,
    PropertyDetailView,
    property_page,
    property_detail_page,
    ChatbotAPIView,
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)

urlpatterns = [
    # DRF router URLs
    path('', include(router.urls)),

    # Chatbot API endpoint
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot_api'),

    # Manual endpoints
    path(
        'properties/<int:pk>/',
        PropertyDetailView.as_view(),
        name='property-detail'
    ),
    path(
        'property-page/',
        property_page,
        name='property-page'
    ),
    # urls.py

    path(
        "property/<int:id>/",
        property_detail_page,
        name="property_detail_short"
    ),
    path(
        "property/<int:id>/<slug:slug>/",
        property_detail_page,
        name="property_detail"
    ),
    
]