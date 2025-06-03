from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Service, Appointment
from .forms import AppointmentForm, RegisterForm

def index(request):
    services = Service.objects.all()
    return render(request, 'salon/index.html', {'services': services})

def services(request):
    services = Service.objects.all()
    return render(request, 'salon/services.html', {'services': services})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def book(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            messages.success(request, 'Вы успешно записались на услугу!')
            return redirect('appointments')
    else:
        form = AppointmentForm()
    return render(request, 'salon/book.html', {'form': form})

@login_required
def appointments(request):
    user_appointments = Appointment.objects.filter(client=request.user).order_by('-date', '-time')
    return render(request, 'salon/appointments.html', {'appointments': user_appointments})

@login_required
def profile(request):
    user_appointments = Appointment.objects.filter(client=request.user).order_by('-date', '-time')
    return render(request, 'salon/profile.html', {
        'user': request.user,
        'appointments': user_appointments
    })

def about(request):
    return render(request, 'salon/about.html')

def contact(request):
    return render(request, 'salon/contact.html')
