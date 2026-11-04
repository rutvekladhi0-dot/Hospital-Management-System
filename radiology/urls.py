from django.urls import path
from . import views

app_name = 'radiology'

urlpatterns = [
    path('tests/', views.radiology_test_list_view, name='test_list'),
    path('tests/create/', views.radiology_test_create_view, name='test_create'),
    path('orders/', views.radiology_order_list_view, name='order_list'),
    path('orders/create/', views.radiology_order_create_view, name='order_create'),
    path('orders/<int:pk>/', views.radiology_order_detail_view, name='order_detail'),
    path('orders/<int:pk>/update/', views.radiology_order_update_view, name='order_update'),
    path('orders/<int:order_pk>/report/upload/', views.radiology_report_upload_view, name='report_upload'),
    path('reports/<int:pk>/', views.radiology_report_detail_view, name='report_detail'),
    path('api/appointments/', views.appointments_by_patient_api, name='appointments_by_patient'),
]
