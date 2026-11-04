from django.contrib import admin
from .models import Ward, Bed, Admission, BedTransfer


class BedInline(admin.TabularInline):
    model = Bed
    extra = 0


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'floor', 'capacity', 'ward_type', 'is_active']
    list_filter = ['ward_type', 'department', 'is_active']
    search_fields = ['name', 'department__name']
    list_editable = ['is_active']
    inlines = [BedInline]


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ['bed_number', 'ward', 'bed_type', 'status', 'daily_rate']
    list_filter = ['ward', 'status', 'bed_type']
    search_fields = ['bed_number', 'ward__name']
    list_editable = ['status']


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'ward', 'bed', 'admission_type', 'status',
                    'admission_date', 'discharge_date']
    list_filter = ['status', 'admission_type', 'ward']
    search_fields = ['patient__patient_id', 'patient__user__first_name',
                     'patient__user__last_name']
    raw_id_fields = ['patient', 'doctor', 'ward', 'bed']
    readonly_fields = ['admission_date', 'discharge_date']
    date_hierarchy = 'admission_date'


@admin.register(BedTransfer)
class BedTransferAdmin(admin.ModelAdmin):
    list_display = ['admission', 'from_ward', 'from_bed', 'to_ward', 'to_bed',
                    'transfer_date', 'transferred_by']
    list_filter = ['transfer_date']
    raw_id_fields = ['admission', 'from_ward', 'from_bed', 'to_ward', 'to_bed', 'transferred_by']
    date_hierarchy = 'transfer_date'
