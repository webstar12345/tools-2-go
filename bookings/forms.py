from django import forms
from .models import Booking
from datetime import timedelta, date

class BookingForm(forms.ModelForm):
    """Form for creating bookings"""
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'rental_period']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'min': (date.today() + timedelta(days=1)).isoformat()}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        rental_period = cleaned_data.get('rental_period')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("End date must be after start date")
            
            # Validate minimum rental period
            days_diff = (end_date - start_date).days
            if rental_period == 'week' and days_diff < 7:
                raise forms.ValidationError("Weekly rentals must be at least 7 days")
            elif rental_period == 'month' and days_diff < 28:
                raise forms.ValidationError("Monthly rentals must be at least 28 days")
            elif rental_period == 'year' and days_diff < 365:
                raise forms.ValidationError("Yearly rentals must be at least 365 days")
        
        return cleaned_data
