from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('medicines/', views.medicine_list_view, name='medicine_list'),
    path('medicines/create/', views.medicine_create_view, name='medicine_create'),
    path('medicines/<int:pk>/', views.medicine_detail_view, name='medicine_detail'),
    path('medicines/<int:pk>/update/', views.medicine_update_view, name='medicine_update'),
    path('medicines/<int:pk>/delete/', views.medicine_delete_view, name='medicine_delete'),
    path('medicines/stock-alert/', views.stock_alert_view, name='stock_alert'),
    path('medicines/expiry-alert/', views.expiry_alert_view, name='expiry_alert'),
    path('suppliers/', views.supplier_list_view, name='supplier_list'),
    path('suppliers/create/', views.supplier_create_view, name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.supplier_update_view, name='supplier_update'),
    path('prescriptions/', views.prescription_list_view, name='prescription_list'),
    path('prescriptions/create/', views.prescription_create_view, name='prescription_create'),
    path('prescriptions/<int:pk>/', views.prescription_detail_view, name='prescription_detail'),
    path('prescriptions/<int:pk>/print/', views.prescription_print_view, name='prescription_print'),
    path('prescriptions/<int:pk>/pdf/', views.prescription_pdf_view, name='prescription_pdf'),
    path('dispense/', views.dispense_view, name='dispense'),
]
