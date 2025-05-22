from django.urls import path
from . import views

app_name = 'tools'  # <-- ✅ ADD THIS LINE!

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('<int:pk>/', views.tool_detail, name='tool_detail'),
    path('create/', views.create_tool, name='create_tool'),
    path('<int:pk>/update/', views.update_tool, name='update_tool'),
    path('<int:pk>/delete/', views.delete_tool, name='delete_tool'),
    path('search/', views.search_tools, name='search_tools'),
    path('<int:tool_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/success/', views.booking_success, name='booking_success'),
]
