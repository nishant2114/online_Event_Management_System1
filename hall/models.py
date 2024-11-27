from django.db import models
from django.conf import settings  # Import settings to reference the custom user model
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User

class Hall(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)  # For example, ratings like 4.5
    description = models.TextField( null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits as per your needs
    capacity = models.PositiveIntegerField()  # Maximum number of people the hall can accommodate
    amenities = models.TextField()  # List of amenities provided (e.g., Wi-Fi, Parking)
    availability = models.BooleanField(default=True)  # To mark if the hall is available for booking
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    images = models.ImageField(upload_to='hall_images/', blank=True, null=True)  # For hall images
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.name

    
    

# Booking Model
class Booking(models.Model):
    hall = models.ForeignKey(
        'Hall', 
        on_delete=models.CASCADE, 
        related_name="bookings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="bookings"
    )  # Links to the custom or default user model
    event_name = models.CharField(
        max_length=255, 
        blank=False, 
        default="Untitled Event"
    )  # New field for event name
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    special_requests = models.TextField(
        blank=True, 
        null=True
    )
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)  # Automatically sets to the current datetime

    class Meta:
        ordering = ['-created_at']  # Orders bookings by the most recent first

    def __str__(self):
        return f"{self.event_name} - {self.user} - {self.hall} ({self.start_date} {self.start_time} - {self.end_date} {self.end_time})"
