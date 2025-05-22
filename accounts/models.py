from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_tool_owner = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
