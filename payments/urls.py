from django.urls import path
from . import views
urlpatterns = [
    # path('payhome/', views.homepage, name='homepage'),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('payment_page/<int:pk>/', views.payment_page, name='payment_page'),  # Payment page for the booking
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),  # Payment verification handler
    path('booking_summary/<int:pk>/', views.booking_summary, name='booking_summary'),  # Booking summary page
    # path('paymenthandler/', views.paymenthandler, name='payment_handler'),
    path('payment_success/<int:pk>/', views.payment_success, name='payment_success'),
    path('payment_fail/', views.payment_fail, name='payment_fail'),
]
