from django.contrib import admin
from .models import NursingStation, NursingTask, VitalSigns


@admin.register(NursingStation)
class NursingStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'ward', 'capacity', 'nurse_in_charge', 'created_at']
    search_fields = ['name']
    raw_id_fields = ['ward', 'nurse_in_charge']


@admin.register(NursingTask)
class NursingTaskAdmin(admin.ModelAdmin):
    list_display = ['patient', 'assigned_to', 'task_type', 'scheduled_time', 'status', 'completed_at']
    list_filter = ['task_type', 'status', 'scheduled_time']
    search_fields = ['patient__patient_id', 'patient__user__first_name', 'patient__user__last_name', 'description']
    raw_id_fields = ['patient', 'assigned_to']
    date_hierarchy = 'scheduled_time'


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                    'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'weight', 'recorded_by', 'recorded_at']
    search_fields = ['patient__patient_id', 'patient__user__first_name', 'patient__user__last_name']
    raw_id_fields = ['patient', 'recorded_by']
    date_hierarchy = 'recorded_at'
    readonly_fields = ['recorded_at']
