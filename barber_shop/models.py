from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='barber_profile')
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='barbers/', verbose_name='Фото')
    experience = models.PositiveIntegerField(verbose_name='Опыт работы (лет)')
    description = models.TextField(verbose_name='Описание')
    specialties = models.TextField(verbose_name='Специализация')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.surname}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = 'Барбер'
        verbose_name_plural = 'Барберы'
        ordering = ['-experience']

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('haircut', 'Стрижка'),
        ('beard', 'Борода'),
        ('combo', 'Комбо'),
        ('coloring', 'Окрашивание'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration = models.PositiveIntegerField(verbose_name='Длительность (минуты)')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    barbers = models.ManyToManyField(Barber, related_name='services', verbose_name='Барберы')
    image = models.ImageField(upload_to='services/', verbose_name='Изображение', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'price']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='Клиент')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='bookings', verbose_name='Барбер')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings', verbose_name='Услуга')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    notes = models.TextField(blank=True, null=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.username} - {self.service.name} ({self.date} {self.time})"

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']
        unique_together = ['barber', 'date', 'time']
