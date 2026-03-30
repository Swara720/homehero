from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Service
from .models import Booking
from .forms import BookingForm

# Customer Dashboard
@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/customer_dashboard.html', {'bookings': bookings})

# Book Service Form
@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.customer = request.user
            booking.save()
            messages.success(request, "Booking request sent to provider!")
            return redirect('bookings:customer_dashboard')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/book_form.html', {'service': service, 'form': form})

# Provider Dashboard
@login_required
def provider_dashboard(request):
    if not request.user.is_provider():
        return redirect('services:home')
    
    pending_bookings = Booking.objects.filter(service__provider=request.user, status='pending')
    confirmed_bookings = Booking.objects.filter(service__provider=request.user, status='confirmed')
    
    return render(request, 'services/provider_dashboard.html', {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
    })

# Accept Booking
@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, service__provider=request.user)
    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, "Booking Accepted! Customer can now make payment.")
    return redirect('services:provider_dashboard')

# Reject Booking
@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, service__provider=request.user)
    if booking.status == 'pending':
        booking.status = 'rejected'
        booking.save()
        messages.success(request, "Booking Rejected.")
    return redirect('services:provider_dashboard')