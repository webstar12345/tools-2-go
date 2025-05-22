from django.shortcuts import render

# Create your views here.
# payments/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import Booking  # Adjust according to your models
import stripe  # Assuming you're using Stripe for payments

# Initialize Stripe with your secret key
stripe.api_key = "your_stripe_secret_key"

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        booking_id = request.POST.get('booking_id')
        booking = Booking.objects.get(id=booking_id)  # Assuming you have a Booking model
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': booking.product_name,  # Adjust with your model
                    },
                    'unit_amount': int(booking.price * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payments/success/'),
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
        )

        return JsonResponse({
            'id': session.id
        })

def payment_success(request):
    # Handle payment success logic (e.g., update booking status)
    return render(request, 'payments/success.html')

def payment_cancel(request):
    # Handle payment cancellation
    return render(request, 'payments/cancel.html')

def make_payment(request, booking_id):
    # Handle the payment page logic
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'payments/payment_page.html', {'booking': booking})
