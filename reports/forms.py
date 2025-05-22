from django import forms
from .models import Report
from datetime import date, timedelta

class ReportForm(forms.ModelForm):
    """Form for generating reports"""
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default dates to last 30 days
        today = date.today()
        thirty_days_ago = today - timedelta(days=30)
        self.fields['start_date'].initial = thirty_days_ago
        self.fields['end_date'].initial = today
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date")
        
        return cleaned_data
