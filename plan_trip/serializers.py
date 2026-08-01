from rest_framework import serializers

from .models import TripPlanRequest


class TripPlanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripPlanRequest
        fields = [
            'id',
            'starting_location',
            'destination',
            'departure_date',
            'duration_days',
            'duration_nights',
            'travelers',
            'group_type',
            'travel_mode',
            'budget',
            'leader_name',
            'leader_phone',
            'notes',
            'submitted_at',
        ]
        read_only_fields = ['id', 'submitted_at']

    def validate_leader_phone(self, value):
        phone = ''.join(ch for ch in value if ch.isdigit())
        if len(phone) < 7:
            raise serializers.ValidationError('Please enter a valid phone number.')
        return value
