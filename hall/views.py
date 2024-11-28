from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Hall
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from decimal import Decimal
from django.utils import timezone
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from accounts.utils.notifications import send_sms

# Get all halls to display on the main hall page

def hall(request):
    location = request.GET.get('location', '').strip()
    date = request.GET.get('date', '').strip()
    time = request.GET.get('time', '').strip()
    suggestions = request.GET.get('suggestions', '').strip()

    # Handle suggestions for autocomplete
    if suggestions:
        locations = Hall.objects.filter(location__icontains=suggestions).values_list('location', flat=True).distinct()
        return JsonResponse(list(locations), safe=False)

    halls = Hall.objects.all()
    
    # Location based filtering
    if location:
        halls = halls.filter(location=location)

    # If both date and time are provided, filter halls based on availability
    if date and time:
        # Combine date and time into a datetime object (assuming 24-hour time format)
        start_datetime = timezone.make_aware(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M"))
        
        # Assume a fixed duration (e.g., 2 hours) for the event
        duration = timezone.timedelta(hours=2)
        end_datetime = start_datetime + duration

        # Exclude halls that are already booked for the given time range
        halls = halls.exclude(
            id__in=Booking.objects.filter(
                start_time__lt=end_datetime,
                end_time__gt=start_datetime
            ).values('hall_id')
        )

    return render(request, 'hall.html', {'halls': halls})





# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def hall_details(request, pk):
    hall = get_object_or_404(Hall, id=pk)
    amenities_list = hall.amenities.split(',')

    # Fetch all bookings for the hall
    bookings = Booking.objects.filter(hall=hall, is_confirmed=True)

    events = [
        {
            "title": booking.event_name,  # Use event_name for the title
            "start": f"{booking.start_date}T{booking.start_time}",
            "end": f"{booking.end_date}T{booking.end_time}",
            "color": "red",  # Color for booked events
        }
        for booking in bookings
    ]

    if request.method == 'POST':
        # Extract form inputs
        event_name = request.POST.get('event_name')  # New field
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        special_requests = request.POST.get('special_requests', '')

        # Validate inputs
        if not (event_name and start_date and start_time and end_date and end_time):
            messages.error(request, "All fields are required.")
            return render(request, 'hall_details.html', {'hall': hall, 'events': events})

        # Parse datetime values
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return render(request, 'hall_details.html', {'hall': hall, 'events': events})

        if end_datetime <= start_datetime:
            messages.error(request, "End time must be after start time.")
            return render(request, 'hall_details.html', {'hall': hall, 'events': events})

        # Check for overlaps
        overlaps = Booking.objects.filter(
            hall=hall,
            start_date__lte=end_datetime.date(),
            end_date__gte=start_datetime.date(),
            is_confirmed=True,
        ).filter(
            start_time__lt=end_datetime.time(),
            end_time__gt=start_datetime.time(),
        )

        if overlaps.exists():
            messages.error(request, "The selected time slot is already booked. Please choose a different time.")
            return render(request, 'hall_details.html', {'hall': hall, 'events': events})

        # Calculate total cost
        duration = Decimal((end_datetime - start_datetime).total_seconds()) / Decimal(3600)  # Convert seconds to hours
        total_cost = duration * hall.price

        # Save booking temporarily without confirming it
        booking = Booking.objects.create(
            hall=hall,
            user=request.user,
            event_name=event_name,  # Save event_name
            start_date=start_datetime.date(),
            start_time=start_datetime.time(),
            end_date=end_datetime.date(),
            end_time=end_datetime.time(),
            special_requests=special_requests,
            total_cost=total_cost,
            is_confirmed=False,  # Not confirmed until payment
        )

        # Send email and SMS notifications
        try:
            send_mail(
                subject='Booking Confirmation',
                message=f"Dear {request.user.username},\n\nYour booking for {hall.name} from {start_datetime} to {end_datetime} has been confirmed.",
                from_email='your-email@gmail.com',
                recipient_list=[request.user.email],
            )
        except Exception as e:
            messages.error(request, 'Error sending email notification.')
            print(f"Email error: {e}")

        try:
            send_sms(
                to=request.user.profile.phone_number,
                message=f"Your booking for {hall.name} from {start_datetime} to {end_datetime} is confirmed."
            )
        except Exception as e:
            messages.error(request, 'Error sending SMS notification.')
            print(f"SMS error: {e}")


        # Redirect to the payment page with booking details
        return redirect('payment_page', pk=booking.id)

    return render(request, 'hall_details.html', {'hall': hall, 'events': events, 'amenities_list': amenities_list})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def hall_bookings(request):
    if request.method == 'POST':
        # Get the booking ID from the POST request
        booking_id = request.POST.get('booking_id')

        # Debugging: Log the booking ID
        print(f"Booking ID received: {booking_id}")

        # If no booking ID is provided, show an error
        if not booking_id:
            messages.error(request, 'No booking ID provided.')
            return redirect('hall_bookings')

        # Retrieve the booking object; if it doesn't exist, show an error
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
            return redirect('hall_bookings')

        # If the booking is confirmed, cancel it
        if booking.is_confirmed:
            booking.is_confirmed = False
            booking.save()
            messages.success(request, 'Your booking has been canceled successfully.')
        else:
            messages.error(request, 'This booking is already canceled.')

        # Redirect back to the bookings page
        return redirect('hall_bookings')

    # Fetch all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'hall_booking.html', {'bookings': bookings})



