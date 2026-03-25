# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Booking
from services.models import Service
from django.contrib.auth.decorators import login_required

@login_required
def book_service(request, service_id):
    if request.user.user_type != 'customer':
        return redirect('/')

    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        date = request.POST.get('date')

        Booking.objects.create(
            service=service,
            user=request.user,
            date=date
        )
        return redirect('/accounts/dashboard/')

    return render(request, 'bookings/book.html', {'service': service})