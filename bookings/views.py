from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Booking, Payment
from .forms import BookingForm
from tools.models import Tool

@login_required
def create_booking(request, tool_id):
    """Create a new booking for a tool"""
    tool = get_object_or_404(Tool, pk=tool_id, available=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tool = tool
            booking.calculate_price()
            booking.save()
            
            # Create a payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                status='pending'
            )
            
            messages.success(request, 'Booking created successfully! Please complete the payment.')
            return redirect('booking_payment', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'tool': tool,
    })

@login_required
def booking_payment(request, booking_id):
    """Handle payment for a booking"""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    
    if request.method == 'POST':
        # In a real application, this would integrate with a payment gateway
        # For now, we'll simulate a successful payment
        payment.status = 'completed'
        payment.transaction_id = f"TRX-{booking.id}-{timezone.now().timestamp()}"
        payment.save()
        
        # Update booking status
        booking.status = 'confirmed'
        booking.save()
        
        messages.success(request, 'Payment successful! Your booking is confirmed.')
        return redirect('booking_detail', booking_id=booking.id)
    
    return render(request, 'bookings/payment.html', {
        'booking': booking,
        'payment': payment,
    })

@login_required
def booking_detail(request, booking_id):
    """View details of a booking"""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
    })

@login_required
def booking_list(request):
    """List all bookings for the current user"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'bookings/booking_list.html', {
        'bookings': bookings,
    })

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        if request.method == 'POST':
            booking.status = 'cancelled'
            booking.save()
            
            # Handle refund if payment was made
            if hasattr(booking, 'payment') and booking.payment.status == 'completed':
                booking.payment.status = 'refunded'
                booking.payment.save()
            
            messages.success(request, 'Booking cancelled successfully!')
            return redirect('booking_list')
        
        return render(request, 'bookings/cancel_booking.html', {
            'booking': booking,
        })
    else:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', booking_id=booking.id)
