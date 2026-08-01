from django.contrib import admin

from .models import TripPlanRequest


@admin.register(TripPlanRequest)
class TripPlanRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'leader_name',
        'starting_location',
        'destination',
        'departure_date',
        'travelers',
        'group_type',
        'travel_mode',
        'submitted_at',
    )
    list_filter = ('group_type', 'travel_mode', 'departure_date')
    search_fields = ('leader_name', 'leader_phone', 'destination', 'starting_location')
