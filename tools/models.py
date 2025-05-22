from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser
from django.conf import settings

class Category(models.Model):
    """Tool category model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Tool(models.Model):
    """Tool model for construction tools"""
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tools')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_year = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-calculate prices if not provided"""
        if not self.price_per_week:
            self.price_per_week = self.price_per_day * 6  # 7 days for price of 6
        if not self.price_per_month:
            self.price_per_month = self.price_per_day * 25  # ~30 days for price of 25
        if not self.price_per_year:
            self.price_per_year = self.price_per_month * 10  # 12 months for price of 10
        super().save(*args, **kwargs)

class ToolImage(models.Model):
    """Images for tools"""
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tool_images/')
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.tool.name}"

class Booking(models.Model):
    tool = models.ForeignKey('Tool', on_delete=models.CASCADE, related_name='bookings_available')  # Use unique related_name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tool_bookings')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user} booked {self.tool} from {self.start_date} to {self.end_date}"
