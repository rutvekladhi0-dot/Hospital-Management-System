from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'created_at', 'ip_address')
    search_fields = ('user__username', 'model_name', 'description', 'ip_address')
    list_filter = ('action', 'model_name', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = (
        'user', 'action', 'model_name', 'object_id', 'description',
        'ip_address', 'user_agent', 'path', 'method', 'created_at'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
