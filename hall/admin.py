from django.contrib import admin

# Register your models here.
from .models import Hall,Booking

admin.site.register(Hall)
admin.site.register(Booking)

