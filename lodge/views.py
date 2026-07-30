from django.shortcuts import render
from rest_framework import serializers
# Create your views here.
from rest_framework import viewsets
from .models import Property
from .serializers import PropertySerializer


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated ,AllowAny
from .models import Property
from .serializers import PropertySerializer,PropertyDetailSerializer
from rest_framework import serializers


from rest_framework import viewsets
from .models import Property
from .serializers import PropertyDetailSerializer

class PropertyViewSet(viewsets.ModelViewSet):

    queryset = Property.objects.all()

    def get_serializer_class(self):

        if self.action == "retrieve":
            return PropertyDetailSerializer

        return PropertySerializer


from rest_framework.generics import RetrieveAPIView
from .models import Property
from .serializers import PropertyDetailSerializer


class PropertyDetailView(RetrieveAPIView):

    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

from django.shortcuts import render

def property_page(request):
    return render(
        request,
        "property_detail.html"
    )

def property_detail_page(request, id):
    return render(
        request,
        "details.html",
        {"property_id": id}
    )

