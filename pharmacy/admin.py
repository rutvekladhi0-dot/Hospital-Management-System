from django.contrib import admin
from django.db import models
from .models import (
    Supplier, Medicine, MedicineCategory, Prescription,
    PrescriptionItem, DispensedMedicine
)


@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'phone']
    list_editable = ['is_active']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'category', 'manufacturer', 'unit_price',
                    'stock_quantity', 'minimum_stock', 'expiry_date', 'batch_number', 'is_active']
    list_filter = ['category', 'is_active', 'expiry_date']
    search_fields = ['name', 'generic_name', 'batch_number', 'manufacturer']
    list_editable = ['stock_quantity', 'is_active']
    filter_horizontal = ['suppliers']
    date_hierarchy = 'created_at'
    actions = ['mark_low_stock_alert', 'export_as_csv']

    def mark_low_stock_alert(self, request, queryset):
        low_stock = queryset.filter(stock_quantity__lt=models.F('minimum_stock'))
        count = low_stock.update(is_active=False)
        if count == 0:
            count = queryset.filter(stock_quantity__lt=models.F('minimum_stock')).count()
        self.message_user(request, f'{count} medicine(s) flagged for low stock.')
    mark_low_stock_alert.short_description = "Flag medicines below minimum stock"

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="medicines.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Generic Name', 'Category', 'Manufacturer', 'Unit Price',
                         'Stock Quantity', 'Minimum Stock', 'Expiry Date', 'Batch Number', 'Active'])
        for med in queryset:
            writer.writerow([
                med.name, med.generic_name, med.category, med.manufacturer,
                med.unit_price, med.stock_quantity, med.minimum_stock,
                med.expiry_date, med.batch_number, med.is_active
            ])
        return response
    export_as_csv.short_description = "Export selected medicines as CSV"


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'diagnosis', 'is_dispensed', 'created_at']
    list_filter = ['is_dispensed', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    raw_id_fields = ['visit', 'doctor', 'patient']
    date_hierarchy = 'created_at'


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'dosage', 'frequency', 'duration', 'quantity']
    search_fields = ['medicine__name']
    raw_id_fields = ['prescription', 'medicine']


@admin.register(DispensedMedicine)
class DispensedMedicineAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'dispensed_by', 'total_cost', 'dispensed_at']
    list_filter = ['dispensed_at']
    raw_id_fields = ['prescription', 'dispensed_by']
    date_hierarchy = 'dispensed_at'
