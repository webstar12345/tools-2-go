from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:tool_id>/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/payment/', views.booking_payment, name='booking_payment'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('', views.booking_list, name='booking_list'),
]
