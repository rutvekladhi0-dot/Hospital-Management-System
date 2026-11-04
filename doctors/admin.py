from django.contrib import admin
from .models import Doctor, DoctorSchedule, DoctorAvailability


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['employee', 'specialization', 'consultation_fee', 'years_of_experience', 'is_available']
    list_filter = ['is_available', 'specialization']
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'employee__user__username']


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['doctor__employee__user__first_name', 'doctor__employee__user__last_name']


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_available', 'max_patients', 'current_patients']
    list_filter = ['date', 'is_available']
    search_fields = ['doctor__employee__user__first_name', 'doctor__employee__user__last_name']
