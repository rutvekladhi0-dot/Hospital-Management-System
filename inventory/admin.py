from django.contrib import admin
from .models import InventoryCategory, InventoryItem, PurchaseOrder


@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'item_type', 'quantity', 'unit', 'unit_price',
                    'reorder_level', 'location', 'is_active', 'created_at']
    list_filter = ['category', 'item_type', 'is_active']
    search_fields = ['name', 'location']
    list_editable = ['quantity', 'is_active']
    date_hierarchy = 'created_at'


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['item', 'supplier_name', 'quantity', 'total_cost', 'order_date',
                    'expected_delivery', 'status', 'ordered_by', 'created_at']
    list_filter = ['status', 'order_date']
    search_fields = ['item__name', 'supplier_name']
    raw_id_fields = ['item', 'ordered_by']
    date_hierarchy = 'order_date'
