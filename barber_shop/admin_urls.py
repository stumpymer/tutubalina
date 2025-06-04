from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('barbers/', views.admin_barber_list, name='admin_barber_list'),
    path('services/', views.admin_service_list, name='admin_service_list'),
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('bookings/<int:booking_id>/update-status/', views.admin_update_booking_status, name='admin_update_booking_status'),
] 