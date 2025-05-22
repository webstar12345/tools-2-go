from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfilePictureForm
from bookings.models import Booking
from tools.models import Tool
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    """Register a new user"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
# @login_required
# def dashboard(request):
#     user = request.user
#     user_tools = Tool.objects.filter(owner=user)
#     user_bookings = Booking.objects.filter(user=user)
#     active_rentals = user_bookings.filter(status='active')

#     context = {
#         'user': user,
#         'user_tools': user_tools,
#         'user_bookings': user_bookings,
#         'active_rentals': active_rentals,
#     }
#     return render(request, 'accounts/dashboard.html', context)
@login_required
def dashboard(request):
    return render(request, 'accounts:dashboard.html', {'user': request.user})


@login_required
def profile(request):
    """User profile view and edit"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def toggle_dark_mode(request):
    """Toggle dark mode preference"""
    if request.method == 'POST':
        user = request.user
        user.dark_mode = not user.dark_mode
        user.save()
        return JsonResponse({'dark_mode': user.dark_mode})
    return JsonResponse({'error': 'Invalid request'}, status=400)
def edit_profile(request):
    # Handle editing the profile
    return render(request, 'accounts:edit_profile.html')

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # Perform login logic (authenticate and redirect)
#             pass
#     else:
#         form = AuthenticationForm()
    
#     return render(request, 'accounts/login.html', {'form': form})
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')  # Make sure 'dashboard' is defined in your URLs
