from django.urls import path
from . import views


urlpatterns = [
  path('',views.home  ,name='home'),
  path('login/',views.login,name='login'),
  path('profile/',views.profile,name='profile'),
  path('logout/',views.logout,name='logout'),
  path('register/',views.register, name='register'),
  path('provider-registration/', views.provider_registration, name='provider_registration'),
]