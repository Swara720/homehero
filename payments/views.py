import razorpay
from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from bookings.models import Booking
from .models import Payment
from django.contrib import messages

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status != 'confirmed':
        messages.error(request, "Only confirmed bookings can be paid.")
        return redirect('bookings:customer_dashboard')

    amount_in_paise = int(booking.service.price * 100)

    order = client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": f"booking_{booking.id}",
        "payment_capture": "1"
    })

    Payment.objects.create(
        booking=booking,
        razorpay_order_id=order['id'],
        amount=booking.service.price,
        status='pending'
    )
    return render(request, 'payments/checkout.html', {
        'key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
        'amount': amount_in_paise,
        'booking': booking,
    })


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'paid'
            payment.paid_at = timezone.now()
            payment.save()

            # Update booking status
            booking = payment.booking
            booking.status = 'paid'
            booking.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print("Payment verification failed:", e)
            return JsonResponse({'status': 'failure'}, status=400)

    return JsonResponse({'status': 'error'}, status=400)