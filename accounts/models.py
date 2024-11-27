from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    USER_TYPES = [
        ('user', 'User'),
        ('hall_provider', 'Hall Provider'),
    ]
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPES, default='user'
    )


    def __str__(self):
        return self.username


# # Create your models here.
# class User_profile(models.Model):
#     user_name = models.CharField(max_length=50, unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     password = models.CharField(max_length=128)


#     def __str__(self):
#         return self.user_name