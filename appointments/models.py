from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.db import models

class Appointment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically reference the user model
        on_delete=models.CASCADE
    )
    hall_id = models.IntegerField()
    status = models.CharField(max_length=10, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default="scheduled")
    type = models.CharField(max_length=10, choices=[
        ('physical', 'Physical'),
        ('virtual', 'Virtual')
    ])
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.date})"
