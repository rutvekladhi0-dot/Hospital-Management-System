from django.contrib import admin
from .models import Ambulance, AmbulanceRequest


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'vehicle_type', 'is_available', 'driver_name',
                    'driver_phone', 'current_location', 'created_at']
    list_filter = ['vehicle_type', 'is_available']
    search_fields = ['vehicle_number', 'driver_name', 'driver_phone']
    list_editable = ['is_available']


@admin.register(AmbulanceRequest)
class AmbulanceRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_phone', 'pickup_location', 'dropoff_location',
                    'ambulance', 'status', 'requested_by', 'dispatched_at', 'completed_at',
                    'distance_km', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['patient_name', 'patient_phone', 'pickup_location', 'dropoff_location']
    raw_id_fields = ['ambulance', 'requested_by']
    date_hierarchy = 'created_at'
    readonly_fields = ['dispatched_at', 'completed_at', 'created_at']
