from django.db import models


class TripPlanRequest(models.Model):
    GROUP_TYPE_CHOICES = [
        ('solo', 'Solo'),
        ('couple', 'Couple'),
        ('family', 'Family'),
        ('boys', 'Boys Group'),
        ('girls', 'Girls Group'),
        ('mixed', 'Mixed Group'),
        ('corporate', 'Corporate Group'),
    ]

    TRAVEL_MODE_CHOICES = [
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('flight', 'Flight'),
        ('lodgehub_car', 'LodgeHub Car Service'),
        ('private_bus', 'Private Travels'),
        ('self_drive', 'Self Drive'),
    ]

    starting_location = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    departure_date = models.DateField()
    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    travelers = models.PositiveIntegerField()
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES)
    travel_mode = models.CharField(max_length=24, choices=TRAVEL_MODE_CHOICES)
    budget = models.CharField(max_length=80, blank=True)
    leader_name = models.CharField(max_length=120)
    leader_phone = models.CharField(max_length=32)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destination} trip request from {self.starting_location}"
