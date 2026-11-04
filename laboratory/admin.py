from django.contrib import admin
from .models import LabTest, LabOrder, LabOrderItem, LabResult


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'price', 'normal_range', 'unit', 'is_active']
    list_filter = ['is_active', 'department']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']


class LabOrderItemInline(admin.TabularInline):
    model = LabOrderItem
    extra = 1
    raw_id_fields = ['test']


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'status', 'priority', 'created_at', 'completed_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    raw_id_fields = ['patient', 'doctor', 'appointment']
    inlines = [LabOrderItemInline]
    date_hierarchy = 'created_at'
    list_editable = ['status']
    actions = ['mark_completed', 'export_as_csv']

    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.exclude(status='Completed').update(status='Completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} lab order(s) marked as completed.')
    mark_completed.short_description = "Mark selected lab orders as completed"

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="lab_orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Patient', 'Doctor', 'Status', 'Priority', 'Created At', 'Completed At'])
        for order in queryset:
            writer.writerow([
                order.id, order.patient, order.doctor, order.status,
                order.priority, order.created_at, order.completed_at
            ])
        return response
    export_as_csv.short_description = "Export selected lab orders as CSV"


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['order_item', 'uploaded_by', 'is_abnormal', 'created_at']
    list_filter = ['is_abnormal', 'created_at']
    raw_id_fields = ['order_item', 'uploaded_by']
    date_hierarchy = 'created_at'
