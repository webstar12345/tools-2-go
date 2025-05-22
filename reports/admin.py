from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'generated_at', 'start_date', 'end_date')
    list_filter = ('report_type', 'generated_at')
    search_fields = ('title', 'generated_by__username')

admin.site.register(Report, ReportAdmin)
