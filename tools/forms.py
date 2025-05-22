from django import forms
from .models import Tool, ToolImage
from .models import Booking  # import your Booking model

class ToolForm(forms.ModelForm):
    """Form for creating and updating tools"""
    class Meta:
        model = Tool
        fields = ['name', 'description', 'category', 'condition', 
                  'price_per_day', 'price_per_week', 'price_per_month', 
                  'price_per_year', 'location', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ToolImageForm(forms.ModelForm):
    """Form for uploading tool images"""
    class Meta:
        model = ToolImage
        fields = ['image', 'is_primary']

ToolImageFormSet = forms.inlineformset_factory(
    Tool, ToolImage, form=ToolImageForm,
    extra=3, can_delete=True, max_num=5
)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'  # or list them like ['tool', 'user', 'start_date', 'end_date']