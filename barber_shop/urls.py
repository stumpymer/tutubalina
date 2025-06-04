from django.urls import path
from . import views

app_name = 'barber_shop'

urlpatterns = [
    # Основные маршруты
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Маршруты для барберов
    path('barbers/', views.barber_list, name='barber_list'),
    path('barbers/<slug:slug>/', views.barber_detail, name='barber_detail'),
    
    # Маршруты для услуг
    path('services/', views.service_list, name='service_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Маршруты для бронирования
    path('booking/create/', views.create_booking, name='create_booking'),
    path('booking/list/', views.booking_list, name='booking_list'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Добавляем маршрут для личного кабинета
    path('account/', views.personal_account, name='personal_account'),
]

# Админ-маршруты (для пользовательской админ панели)
# app_name = 'custom_admin' # Moved to admin_urls.py
# admin_urlpatterns = [
#     path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     path('admin/barbers/', views.admin_barber_list, name='admin_barber_list'),
#     path('admin/services/', views.admin_service_list, name='admin_service_list'),
#     path('admin/bookings/', views.admin_booking_list, name='admin_booking_list'),
#     path('admin/bookings/<int:booking_id>/update-status/', views.admin_update_booking_status, name='admin_update_booking_status'),
# ] 