from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser
from tools.models import Tool
from django.utils import timezone

class Booking(models.Model):
    """Booking model for tool rentals"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    RENTAL_PERIOD_CHOICES = (
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='bookings_booked')  # Use unique related_name
    start_date = models.DateField()
    end_date = models.DateField()
    rental_period = models.CharField(max_length=10, choices=RENTAL_PERIOD_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tool.name} ({self.start_date} to {self.end_date})"

    
    def save(self, *args, **kwargs):
        """Calculate total price if not provided"""
        if not self.total_price:
            self.calculate_price()
        super().save(*args, **kwargs)
    
    def calculate_price(self):
        """Calculate the total price based on rental period"""
        if self.rental_period == 'day':
            days = (self.end_date - self.start_date).days
            self.total_price = self.tool.price_per_day * days
        elif self.rental_period == 'week':
            weeks = ((self.end_date - self.start_date).days) // 7
            self.total_price = self.tool.price_per_week * weeks
        elif self.rental_period == 'month':
            # Approximate months
            months = ((self.end_date - self.start_date).days) // 30
            self.total_price = self.tool.price_per_month * months
        elif self.rental_period == 'year':
            # Approximate years
            years = ((self.end_date - self.start_date).days) // 365
            self.total_price = self.tool.price_per_year * years
        
        return self.total_price
    
    def is_overdue(self):
        """Check if the booking is overdue"""
        return self.status == 'active' and self.end_date < timezone.now().date()

class Payment(models.Model):
    """Payment model for bookings"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Payment for {self.booking}"
