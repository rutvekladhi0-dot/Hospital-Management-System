from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/create/', views.category_create_view, name='category_create'),
    path('items/', views.item_list_view, name='item_list'),
    path('items/create/', views.item_create_view, name='item_create'),
    path('items/<int:pk>/', views.item_detail_view, name='item_detail'),
    path('items/<int:pk>/update/', views.item_update_view, name='item_update'),
    path('purchase-orders/', views.purchase_order_list_view, name='purchase_order_list'),
    path('purchase-orders/create/', views.purchase_order_create_view, name='purchase_order_create'),
    path('purchase-orders/<int:pk>/update/', views.purchase_order_update_view, name='purchase_order_update'),
    path('stock-alerts/', views.stock_alert_view, name='stock_alert'),
]
