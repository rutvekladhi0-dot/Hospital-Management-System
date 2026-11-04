from django.db import models
from django.conf import settings


class InventoryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Inventory Category'
        verbose_name_plural = 'Inventory Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Equipment', 'Equipment'),
        ('Consumable', 'Consumable'),
        ('Supplies', 'Supplies'),
        ('Furniture', 'Furniture'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=15, choices=ITEM_TYPE_CHOICES, default='Consumable')
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.IntegerField(default=10)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    @property
    def total_value(self):
        return self.quantity * self.unit_price


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ordered', 'Ordered'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='purchase_orders')
    supplier_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateField()
    expected_delivery = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='purchase_orders')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-order_date']

    def __str__(self):
        return f"PO - {self.item.name} ({self.supplier_name})"
