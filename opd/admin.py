from django.contrib import admin
from .models import OPDVisit


@admin.register(OPDVisit)
class OPDVisitAdmin(admin.ModelAdmin):
    list_display = ['opd_number', 'patient', 'doctor', 'visit_date', 'status', 'created_at']
    list_filter = ['status', 'visit_date']
    search_fields = ['opd_number', 'patient__patient_id', 'patient__user__first_name',
                     'patient__user__last_name', 'doctor__employee__user__first_name']
    raw_id_fields = ['patient', 'doctor', 'appointment']
    date_hierarchy = 'visit_date'
    readonly_fields = ['opd_number', 'created_at']
