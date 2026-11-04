from django.contrib import admin
from .models import Designation, HRRecord, Training


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'description']
    search_fields = ['name']
    raw_id_fields = ['department']


@admin.register(HRRecord)
class HRRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'record_type', 'effective_date', 'created_by', 'created_at']
    list_filter = ['record_type', 'effective_date']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name', 'description']
    raw_id_fields = ['employee', 'created_by']
    date_hierarchy = 'effective_date'


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'trainer', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'start_date']
    search_fields = ['title', 'trainer', 'description']
    filter_horizontal = ['employees']
    date_hierarchy = 'start_date'
