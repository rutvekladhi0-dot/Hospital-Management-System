from django.contrib import admin
from .models import Employee, Attendance, LeaveRequest


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'designation', 'date_of_joining', 'salary', 'is_active', 'created_at']
    list_filter = ['is_active', 'department', 'designation']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'designation']
    readonly_fields = ['employee_id']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'date']
    search_fields = ['employee__employee_id', 'employee__user__first_name']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by', 'created_at']
    list_filter = ['status', 'leave_type']
    search_fields = ['employee__employee_id', 'employee__user__first_name']
