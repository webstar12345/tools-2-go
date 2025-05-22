from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Report(models.Model):
    """Model for storing generated reports"""
    REPORT_TYPES = (
        ('summary', 'Summary Report'),
        ('detailed', 'Detailed Report'),
        ('exception', 'Exception Report'),
    )
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='reports')
    generated_at = models.DateTimeField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.generated_at.strftime('%Y-%m-%d')}"
