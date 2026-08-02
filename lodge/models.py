from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('lodge', 'Lodge'),
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('hostel', 'Hostel'),
    
    ]

    CATEGORY_CHOICES = [
        ('luxury', 'Luxury'),
        ('budget', 'Budget'),
        ('family', 'Family'),
        ('business', 'Business'),
        ('pet-friendly', 'Pet Friendly'),
        ('beachfront', 'Beachfront'),
        ('hillside', 'Hillside'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    reviews_count = models.PositiveIntegerField(default=0)

    badge = models.CharField(max_length=50, blank=True)

    features = models.ManyToManyField('Feature',blank=True,related_name="properties")
    

    amenities = models.ManyToManyField(Amenity, related_name='properties', blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    check_in_time = models.TimeField(null=True, blank=True)

    check_out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name


# 🔥 NEW MODEL FOR IMAGES
class PropertyImage(models.Model):
    IMAGE_TYPES = [
        ('room', 'Room'),
        ('facility', 'Facility'),
        ('exterior', 'Exterior'),
        ('lobby', 'Lobby'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='property_images/')

    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPES,
        default='room'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)



class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Room(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    room_name = models.CharField(max_length=100)

    description = models.TextField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField()

    total_rooms = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.property.name} - {self.room_name}"


class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='room_images/'
    )

