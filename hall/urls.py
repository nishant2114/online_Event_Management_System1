from django.urls import path
from . import views


urlpatterns = [
  path('hall', views.hall, name='hall'),
  path('hall_details/<str:pk>/', views.hall_details, name='hall_details'),
  path('hall_bookings', views.hall_bookings, name='hall_bookings'),
]