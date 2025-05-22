from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')

class CustomUserChangeForm(UserChangeForm):
    """Form for updating user information"""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'profile_picture')

class ProfilePictureForm(forms.ModelForm):
    """Form for updating profile picture"""
    class Meta:
        model = CustomUser
        fields = ('profile_picture',)
