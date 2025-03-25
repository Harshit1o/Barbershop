from django.contrib import admin
from .models import Service, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('service', 'status')
    search_fields = ('user__username', 'service__name')
    ordering = ('appointment_date', 'appointment_time')

