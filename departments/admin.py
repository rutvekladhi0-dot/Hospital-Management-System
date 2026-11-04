from django.contrib import admin
from .models import Department, Specialization


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'head', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'branch']
    search_fields = ['name', 'email', 'phone']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'is_active']
    list_filter = ['is_active', 'department']
    search_fields = ['name']
