from django.contrib import admin
from .models import InsuranceProvider, InsurancePlan, PatientInsurance


class InsurancePlanInline(admin.TabularInline):
    model = InsurancePlan
    extra = 0


@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_person', 'phone', 'email']
    list_editable = ['is_active']
    inlines = [InsurancePlanInline]


@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'coverage_percentage', 'max_coverage', 'is_active']
    list_filter = ['provider', 'is_active']
    search_fields = ['name', 'provider__name']
    list_editable = ['is_active']


@admin.register(PatientInsurance)
class PatientInsuranceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'plan', 'policy_number', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date']
    search_fields = ['patient__patient_id', 'patient__user__first_name',
                     'patient__user__last_name', 'policy_number']
    raw_id_fields = ['patient', 'plan']
    list_editable = ['is_active']
