from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('book/', views.book, name='book'),
    path('appointments/', views.appointments, name='appointments'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    # Use Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
] 