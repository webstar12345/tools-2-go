from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking, Payment

class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tool', 'start_date', 'end_date', 'rental_period', 'total_price', 'status')
    list_filter = ('status', 'rental_period', 'start_date')
    search_fields = ('user__username', 'tool__name')
    inlines = [PaymentInline]

admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment)
