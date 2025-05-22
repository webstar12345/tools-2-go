# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL for creating a checkout session (Stripe or another service)
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),

    # URL for payment success
    path('success/', views.payment_success, name='payment_success'),

    # URL for payment cancellation
    path('cancel/', views.payment_cancel, name='payment_cancel'),

    # URL for handling individual payment requests based on booking ID (if needed)
    path('<int:booking_id>/pay/', views.make_payment, name='make_payment'),
]
