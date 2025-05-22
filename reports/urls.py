from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_dashboard, name='report_dashboard'),
    path('generate/', views.generate_report, name='generate_report'),
    path('list/', views.report_list, name='report_list'),
]
