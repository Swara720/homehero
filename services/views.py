from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm
from bookings.models import Booking

def home(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'home.html', {'services': services})

@login_required
def provider_dashboard(request):
    if not request.user.is_provider():
        return redirect('services:home')

    # Pending bookings for this provider
    pending_bookings = Booking.objects.filter(
        service__provider=request.user, 
        status='pending'
    ).order_by('-created_at')

    # Confirmed bookings
    confirmed_bookings = Booking.objects.filter(
        service__provider=request.user, 
        status='confirmed'
    ).order_by('-created_at')

    my_services = Service.objects.filter(provider=request.user)

    return render(request, 'services/provider_dashboard.html', {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'my_services': my_services,
    })

@login_required
def create_service(request):
    if not request.user.is_provider():
        return redirect('services:home')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            return redirect('services:provider_dashboard')
    else:
        form = ServiceForm()
    
    return render(request, 'services/create_service.html', {'form': form})

def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'services/list.html', {'services': services})