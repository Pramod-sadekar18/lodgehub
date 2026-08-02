from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
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

def property_detail_page(request, id, slug=None):
    property_obj = get_object_or_404(Property, id=id)

    if not property_obj.slug:
        property_obj.slug = slugify(property_obj.name) or "property"
        property_obj.save(update_fields=["slug"])

    if slug and property_obj.slug != slug:
        return redirect("property_detail", id=property_obj.id, slug=property_obj.slug)

    if not slug:
        return redirect("property_detail", id=property_obj.id, slug=property_obj.slug)

    return render(
        request,
        "details.html",
        {"property_id": id, "property_slug": property_obj.slug}
    )

