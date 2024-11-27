from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
import razorpay
from hall.models import Booking

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def payment_page(request, pk):
    # Fetch the booking details
    booking = get_object_or_404(Booking, id=pk)

    # Check if the booking is already confirmed
    if booking.is_confirmed:
        return redirect('booking_summary', pk=booking.id)

    amount = int(booking.total_cost * 100)  # Convert to paise (Razorpay expects this)

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency='INR',
        payment_capture='1'
    ))
    razorpay_order_id = razorpay_order['id']

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'razorpay_amount': amount,
        'currency': 'INR',
        'booking_id': booking.id,
        'callback_url': '/paymenthandler/',
        'booking': booking,  # Include booking details
    }
    return render(request, 'payment_page.html', context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            booking_id = request.POST.get('booking_id', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Capture the payment
            booking = Booking.objects.get(id=booking_id)
            amount = int(booking.total_cost * 100)
            razorpay_client.payment.capture(payment_id, amount)

            # Mark the booking as confirmed
            booking.is_confirmed = True
            booking.save()

            return redirect('payment_success', pk=booking.id)

        except Exception as e:
            return render(request, 'payment_fail.html', {'error': str(e)})

    return HttpResponseBadRequest("Invalid request method")

@login_required
def booking_summary(request, pk):
    booking = get_object_or_404(Booking, id=pk, user=request.user, is_confirmed=True)
    return render(request, 'booking_summary.html', {'booking': booking})

def payment_success(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.is_confirmed = True
    booking.save()
    return render(request, 'payment_success.html', {'booking': booking})

def payment_fail(request):
    return render(request, 'payment_fail.html')
