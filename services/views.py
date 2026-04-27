from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceImage
from .forms import ServiceForm
from bookings.models import Booking, Favorite
from django.contrib import messages

def home(request):
    services = Service.objects.all()

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(
            user=request.user
        ).values_list('service_id', flat=True)

    return render(request, "home.html", {
        "services": services,
        "favorite_ids": favorite_ids
    })

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


# Toggle Favorite
@login_required
def toggle_favorite(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, service=service)
    
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites!")
    
    return redirect('services:home')