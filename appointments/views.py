from django.shortcuts import render, redirect, get_object_or_404
from hall.models import Hall
from .models import Appointment
from django.http import JsonResponse
from .models import Appointment
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse

@login_required
def dashboard(request):
    today = date.today()
    current_events = Appointment.objects.filter(user=request.user, date=today)
    future_events = Appointment.objects.filter(user=request.user, date__gt=today)
    past_events = Appointment.objects.filter(user=request.user, date__lt=today)

    context = {
        'current_events': current_events,
        'future_events': future_events,
        'past_events': past_events
    }
    return render(request, 'appointments_dashboard.html', context)

@login_required
def get_appointments(request):
    appointments = list(Appointment.objects.filter(user=request.user).values())
    return JsonResponse(appointments, safe=False)

@login_required

def create_appointment(request, pk):
    # Fetch the hall object using pk or return a 404 if not found
    hall = get_object_or_404(Hall, id=pk)

    if request.method == 'POST':
        title = request.POST['title']
        date = request.POST['date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        status = request.POST['status']
        type = request.POST['type']
        description = request.POST.get('description', '')

        # Create a new appointment instance
        new_appointment = Appointment.objects.create(
            user=request.user,
            title=title,
            date=date,
            start_time=start_time,
            end_time=end_time,
            hall_id=hall.id,
            status=status,
            type=type,
            description=description
        )

        # Redirect to the dashboard with the hall's ID
        return redirect('appointments_dashboard', pk=hall.id)

    return render(request, 'create_appointment.html', {'hall': hall})

