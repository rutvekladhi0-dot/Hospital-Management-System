from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Q, Sum

from .models import InventoryCategory, InventoryItem, PurchaseOrder
from .forms import InventoryCategoryForm, InventoryItemForm, PurchaseOrderForm
from core.mixins import AdminRequiredMixin


class CategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = InventoryCategory
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'
    paginate_by = 25

    def get_queryset(self):
        return InventoryCategory.objects.all()


category_list_view = CategoryListView.as_view()


class CategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = InventoryCategory
    form_class = InventoryCategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully.')
        return super().form_valid(form)


category_create_view = CategoryCreateView.as_view()


class ItemListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
    paginate_by = 25

    def get_queryset(self):
        queryset = InventoryItem.objects.select_related('category')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        item_type = self.request.GET.get('item_type')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search)
            )
        if category:
            queryset = queryset.filter(category_id=category)
        if item_type:
            queryset = queryset.filter(item_type=item_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'itemTable'
        context['categories'] = InventoryCategory.objects.all()
        context['item_types'] = InventoryItem.ITEM_TYPE_CHOICES
        context['low_stock_count'] = InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level'), is_active=True
        ).count()
        return context


item_list_view = ItemListView.as_view()


class ItemCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('inventory:item_list')

    def form_valid(self, form):
        messages.success(self.request, 'Item created successfully.')
        return super().form_valid(form)


item_create_view = ItemCreateView.as_view()


class ItemUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('inventory:item_list')

    def form_valid(self, form):
        messages.success(self.request, 'Item updated successfully.')
        return super().form_valid(form)


item_update_view = ItemUpdateView.as_view()


class ItemDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = InventoryItem
    template_name = 'inventory/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_orders'] = self.object.purchase_orders.all()[:10]
        return context


item_detail_view = ItemDetailView.as_view()


class PurchaseOrderListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'inventory/purchase_order_list.html'
    context_object_name = 'purchase_orders'
    paginate_by = 25

    def get_queryset(self):
        queryset = PurchaseOrder.objects.select_related('item', 'ordered_by')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'poTable'
        context['status_choices'] = PurchaseOrder.STATUS_CHOICES
        return context


purchase_order_list_view = PurchaseOrderListView.as_view()


class PurchaseOrderCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'inventory/purchase_order_form.html'
    success_url = reverse_lazy('inventory:purchase_order_list')

    def form_valid(self, form):
        form.instance.ordered_by = self.request.user
        messages.success(self.request, 'Purchase order created successfully.')
        return super().form_valid(form)


purchase_order_create_view = PurchaseOrderCreateView.as_view()


class PurchaseOrderUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'inventory/purchase_order_form.html'
    success_url = reverse_lazy('inventory:purchase_order_list')

    def form_valid(self, form):
        if form.instance.status == 'Delivered' and self.object.status != 'Delivered':
            self.object.item.quantity += self.object.quantity
            self.object.item.save()
        messages.success(self.request, 'Purchase order updated successfully.')
        return super().form_valid(form)


purchase_order_update_view = PurchaseOrderUpdateView.as_view()


class StockAlertView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/stock_alert.html'
    context_object_name = 'low_stock_items'

    def get_queryset(self):
        return InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level'),
            is_active=True
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'stockAlertTable'
        context['out_of_stock_count'] = InventoryItem.objects.filter(
            quantity=0, is_active=True
        ).count()
        context['low_stock_count'] = InventoryItem.objects.filter(
            quantity__gt=0,
            quantity__lte=models.F('reorder_level'),
            is_active=True
        ).count()
        return context


stock_alert_view = StockAlertView.as_view()
