from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Property, Amenity, PropertyImage , Feature ,Room ,RoomImage


# ---------- AMENITY ----------
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ---------- PROPERTY IMAGES (INLINE) ----------
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


# ---------- PROPERTY ----------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'city',
        'property_type',
        'category',
        'price_per_night',
        'is_verified',
        'created_at'
    )

    list_filter = (
        'city',
        'property_type',
        'category',
        'is_verified'
    )

    search_fields = (
        'name',
        'city',
        'location',
        'address'
    )

    list_editable = ('is_verified',)

    filter_horizontal = ('amenities','features')

    inlines = [PropertyImageInline]

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'owner',
                'name',
                'description',
                'property_type',
                'category',
                'is_verified'
            )
        }),

        ('Location Details', {
            'fields': (
                'city',
                'location',
                'address',
                'latitude',
                'longitude'
            )
        }),

        ('Pricing & Stats', {
            'fields': (
                'price_per_night',
                'rating',
                'reviews_count',
                'badge'
            )
        }),

        ('Timings', {
            'fields': (
                'check_in_time',
                'check_out_time'
            )
        }),

        ('Relations', {
            'fields': (
                'amenities',
                'features',
            )
        }),
    )

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'room_name',
        'property',
        'price_per_night',
        'capacity',
        'total_rooms'
    )

    search_fields = (
        'room_name',
        'property__name'
    )

    list_filter = (
        'property',
    )

    inlines = [RoomImageInline]


