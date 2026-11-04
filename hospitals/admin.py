from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_main_branch', 'is_active', 'created_at']
    list_filter = ['is_main_branch', 'is_active']
    search_fields = ['name', 'phone']
