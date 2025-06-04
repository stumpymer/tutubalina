from django.contrib import admin
from .models import Barber, Service, Booking

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'experience', 'is_active', 'created_at')
    list_filter = ('is_active', 'experience')
    search_fields = ('name', 'surname', 'description', 'specialties')
    prepopulated_fields = {'slug': ('name', 'surname')}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'name', 'surname', 'photo', 'slug')
        }),
        ('Профессиональная информация', {
            'fields': ('experience', 'description', 'specialties')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('barbers',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'image')
        }),
        ('Детали услуги', {
            'fields': ('description', 'price', 'duration', 'barbers')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'barber', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'barber')
    search_fields = ('client__username', 'barber__name', 'service__name', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Информация о записи', {
            'fields': ('client', 'barber', 'service', 'date', 'time')
        }),
        ('Статус и примечания', {
            'fields': ('status', 'notes')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = 'Отметить как подтвержденные'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = 'Отметить как выполненные'

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Отметить как отмененные'
