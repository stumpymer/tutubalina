from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Barber, Service, Booking
from .forms import (
    UserRegistrationForm, CustomAuthenticationForm,
    BookingForm, BarberProfileForm, ServiceForm
)

def home(request):
    barbers = Barber.objects.filter(is_active=True)[:4]
    services = Service.objects.filter(is_active=True)[:6]
    context = {
        'barbers': barbers,
        'services': services,
    }
    return render(request, 'barber_shop/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('barber_shop:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'barber_shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('barber_shop:home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'barber_shop/login.html', {'form': form})

@login_required(login_url='barber_shop:login')
def user_logout(request):
    logout(request)
    return redirect('barber_shop:home')

def barber_list(request):
    barbers = Barber.objects.filter(is_active=True)
    paginator = Paginator(barbers, 6)
    page = request.GET.get('page')
    barbers = paginator.get_page(page)
    return render(request, 'barber_shop/barber_list.html', {'barbers': barbers})

def barber_detail(request, slug):
    barber = get_object_or_404(Barber, slug=slug, is_active=True)
    services = barber.services.filter(is_active=True)
    return render(request, 'barber_shop/barber_detail.html', {
        'barber': barber,
        'services': services
    })

def service_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    
    services = Service.objects.filter(is_active=True)
    
    if category:
        services = services.filter(category=category)
    
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(services, 9)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    
    return render(request, 'barber_shop/service_list.html', {
        'services': services,
        'categories': Service.CATEGORY_CHOICES
    })

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    barbers = service.barbers.filter(is_active=True)
    return render(request, 'barber_shop/service_detail.html', {
        'service': service,
        'barbers': barbers
    })

@login_required(login_url='barber_shop:login')
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.save()
            return redirect('barber_shop:booking_list')
    else:
        form = BookingForm()
        # Если барбер или услуга выбраны в URL, устанавливаем их в форму
        barber_id = request.GET.get('barber')
        service_id = request.GET.get('service')
        if barber_id:
            form.fields['barber'].initial = barber_id
        if service_id:
            form.fields['service'].initial = service_id
    return render(request, 'barber_shop/create_booking.html', {'form': form})

@login_required(login_url='barber_shop:login')
def booking_list(request):
    bookings = Booking.objects.filter(client=request.user).order_by('-date', '-time')
    return render(request, 'barber_shop/booking_list.html', {'bookings': bookings})

@login_required(login_url='barber_shop:login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
    return redirect('barber_shop:booking_list')

@login_required(login_url='barber_shop:login')
def personal_account(request):
    # Placeholder view for personal account
    # You can add logic here to display user-specific data, e.g., bookings
    user_bookings = request.user.bookings.all().order_by('-date', '-time')
    context = {
        'user_bookings': user_bookings,
    }
    return render(request, 'barber_shop/personal_account.html', context)

# Админ-представления
@login_required(login_url='barber_shop:login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('barber_shop:home')
    
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_barbers = Barber.objects.count()
    total_services = Service.objects.count()
    
    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_barbers': total_barbers,
        'total_services': total_services,
    }
    return render(request, 'barber_shop/admin/dashboard.html', context)

@login_required(login_url='barber_shop:login')
def admin_barber_list(request):
    if not request.user.is_staff:
        return redirect('barber_shop:home')
    
    barbers = Barber.objects.all()
    return render(request, 'barber_shop/admin/barber_list.html', {'barbers': barbers})

@login_required(login_url='barber_shop:login')
def admin_service_list(request):
    if not request.user.is_staff:
        return redirect('barber_shop:home')
    
    services = Service.objects.all()
    return render(request, 'barber_shop/admin/service_list.html', {'services': services})

@login_required(login_url='barber_shop:login')
def admin_booking_list(request):
    if not request.user.is_staff:
        return redirect('barber_shop:home')
    
    bookings = Booking.objects.all().order_by('-date', '-time')
    return render(request, 'barber_shop/admin/booking_list.html', {'bookings': bookings})

@login_required(login_url='barber_shop:login')
def admin_update_booking_status(request, booking_id):
    if not request.user.is_staff:
        return redirect('barber_shop:home')
    
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
    return redirect('barber_shop:admin_booking_list')
