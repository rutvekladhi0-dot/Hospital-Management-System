from django.contrib import admin
from .models import Patient, MedicalRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'user', 'blood_group', 'emergency_contact_name', 'created_at']
    list_filter = ['blood_group', 'created_at']
    search_fields = ['patient_id', 'user__first_name', 'user__last_name', 'user__username']
    readonly_fields = ['patient_id']
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="patients.csv"'
        writer = csv.writer(response)
        writer.writerow(['Patient ID', 'User', 'Blood Group', 'Emergency Contact', 'Emergency Phone', 'Created At'])
        for patient in queryset:
            writer.writerow([
                patient.patient_id, patient.user, patient.blood_group,
                patient.emergency_contact_name, patient.emergency_contact_phone,
                patient.created_at
            ])
        return response
    export_as_csv.short_description = "Export selected patients as CSV"


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis', 'created_at']
    list_filter = ['visit_date']
    search_fields = ['patient__patient_id', 'patient__user__first_name', 'diagnosis']
