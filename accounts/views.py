from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm   # We'll create this if missing
from bookings.models import Booking
from accounts.models import User

@login_required
def admin_dashboard(request):
    # Sirf admin ya superuser ko allow karo
    if not (request.user.is_superuser or request.user.user_type == 'admin'):
        return redirect('services:home')

    total_customers = User.objects.filter(user_type='customer').count()
    total_providers = User.objects.filter(user_type='provider').count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    paid_bookings = Booking.objects.filter(status='paid').count()
    
    total_revenue = Booking.objects.filter(status='paid').aggregate(Sum('service__price'))['service__price__sum'] or 0

    context = {
        'total_customers': total_customers,
        'total_providers': total_providers,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'paid_bookings': paid_bookings,
        'total_revenue': total_revenue,
    }
    return render(request, 'admin/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            # Fixed: Safe redirect after registration
            if user.is_provider():
                return redirect('services:provider_dashboard')
            else:
                return redirect('bookings:customer_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Role based redirect after login
            if user.is_provider():
                return redirect('services:provider_dashboard')
            elif user.is_admin():
                return redirect('admin_dashboard')
            else:
                return redirect('bookings:customer_dashboard')
        else:
            messages.error(request, "Invalid username or password!")
    
    return render(request, 'accounts/login.html')

@login_required
def dashboard_redirect(request):
    # Strong Admin Check
    if request.user.is_superuser or request.user.user_type == 'admin':
        return redirect('admin_dashboard')

    # Provider
    if request.user.is_provider():
        return redirect('services:provider_dashboard')

    # Customer (default)
    return redirect('bookings:customer_dashboard')

@login_required
def user_logout(request):
    logout(request)
    return redirect('services:home')