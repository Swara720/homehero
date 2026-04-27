from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from services.models import Service
from .models import Booking, Favorite
from .forms import BookingForm
from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
from payments.models import Payment
from .models import Review

@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')

    for booking in bookings:
        payment = Payment.objects.filter(booking_id=booking.id, status="paid").first()

        booking.is_paid = payment is not None
        booking.is_reviewed = Review.objects.filter(booking=booking).exists()

    return render(request, 'bookings/customer_dashboard.html', {'bookings': bookings})


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

@login_required
def toggle_favorite(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    fav = Favorite.objects.filter(user=request.user, service=service).first()

    if fav:
        fav.delete()
        return JsonResponse({"status": "removed"})
    else:
        Favorite.objects.create(user=request.user, service=service)
        return JsonResponse({"status": "added"})

@login_required
def submit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    # allow only if payment done
    payment = Payment.objects.filter(booking=booking, status="paid").first()
    if not payment:
        return redirect('bookings:customer_dashboard')

    # prevent duplicate
    if Review.objects.filter(booking=booking).exists():
        return redirect('bookings:customer_dashboard')

    if request.method == "POST":
        Review.objects.create(
            booking=booking,
            user=request.user,
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment")
        )
        return redirect('bookings:customer_dashboard')

    return render(request, "bookings/review_form.html", {"booking": booking})