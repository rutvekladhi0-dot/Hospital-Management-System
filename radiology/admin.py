from django.contrib import admin
from .models import RadiologyTest, RadiologyOrder, RadiologyReport


@admin.register(RadiologyTest)
class RadiologyTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']


@admin.register(RadiologyOrder)
class RadiologyOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'test', 'status', 'priority', 'created_at', 'completed_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'test__name']
    raw_id_fields = ['patient', 'doctor', 'test', 'appointment']
    date_hierarchy = 'created_at'
    list_editable = ['status']


@admin.register(RadiologyReport)
class RadiologyReportAdmin(admin.ModelAdmin):
    list_display = ['order', 'reported_by', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['order', 'reported_by']
    date_hierarchy = 'created_at'
