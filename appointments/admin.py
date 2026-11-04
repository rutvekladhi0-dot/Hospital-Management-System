from django.contrib import admin
from .models import Appointment, Visit


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_type', 'status']
    list_filter = ['status', 'appointment_type', 'appointment_date']
    search_fields = [
        'patient__patient_id', 'patient__user__first_name', 'patient__user__last_name',
        'doctor__employee__user__first_name', 'doctor__employee__user__last_name'
    ]


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis', 'follow_up_date', 'created_at']
    list_filter = ['created_at']
    search_fields = ['appointment__patient__patient_id', 'diagnosis']
