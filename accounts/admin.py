# from django.contrib import admin

# # Register your models here.
# from .models import User_profile

# @admin.register(User_profile)
# class CustomTableAdmin(admin.ModelAdmin):
#     list_display = ('user_name', 'first_name', ' last_name', 'email','phone_number ','address','password')
#     search_fields = ('user_name',)
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'description', 'address', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'description', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'description', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

# Register your CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
