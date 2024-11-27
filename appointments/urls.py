from django.urls import path
from . import views


urlpatterns = [
    path('appointments_dashboard/', views.dashboard, name='appointments_dashboard'),
    path('api/appointments/', views.get_appointments, name='get_appointments'),
    path('create_appointment/<str:pk>/', views.create_appointment, name='create_appointment'),
]
