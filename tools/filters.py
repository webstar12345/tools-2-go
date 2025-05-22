import django_filters
from django import forms
from .models import Tool, Category

class ToolFilter(django_filters.FilterSet):
    """Filter for tools"""
    RENTAL_PERIOD_CHOICES = (
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year'),
    )
    
    name = django_filters.CharFilter(lookup_expr='icontains', label='Tool Name')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    price = django_filters.RangeFilter(method='filter_by_price')
    rental_period = django_filters.ChoiceFilter(choices=RENTAL_PERIOD_CHOICES, method='filter_rental_period', label='Rental Period')
    condition = django_filters.MultipleChoiceFilter(choices=Tool.CONDITION_CHOICES, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Tool
        fields = ['name', 'category', 'condition']
    
    def filter_by_price(self, queryset, name, value):
        """Filter by price based on rental period"""
        rental_period = self.data.get('rental_period', 'day')
        
        if rental_period == 'day':
            field_name = 'price_per_day'
        elif rental_period == 'week':
            field_name = 'price_per_week'
        elif rental_period == 'month':
            field_name = 'price_per_month'
        else:
            field_name = 'price_per_year'
        
        filters = {}
        if value.start:
            filters[f'{field_name}__gte'] = value.start
        if value.stop:
            filters[f'{field_name}__lte'] = value.stop
        
        return queryset.filter(**filters)
    
    def filter_rental_period(self, queryset, name, value):
        """Just a placeholder to capture the rental period choice"""
        return queryset
