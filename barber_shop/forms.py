from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking, Barber, Service

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['barber', 'service', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['barber'].queryset = Barber.objects.filter(is_active=True)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)

class BarberProfileForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = ['name', 'surname', 'photo', 'experience', 'description', 'specialties']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specialties': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'category', 'barbers', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'barbers': forms.SelectMultiple(attrs={'class': 'form-control'}),
        } 