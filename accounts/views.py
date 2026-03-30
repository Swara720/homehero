from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm   # We'll create this if missing

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
            else:
                return redirect('bookings:customer_dashboard')
        else:
            messages.error(request, "Invalid username or password!")
    
    return render(request, 'accounts/login.html')

@login_required
def dashboard_redirect(request):
    if request.user.is_provider():
        return redirect('provider_dashboard')
    elif request.user.is_customer():
        return redirect('accounts:customer_dashboard')
    return redirect('admin:index')

@login_required
def user_logout(request):
    logout(request)
    return redirect('services:home')