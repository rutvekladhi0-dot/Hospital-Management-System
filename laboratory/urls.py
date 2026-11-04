from django.urls import path
from . import views

app_name = 'laboratory'

urlpatterns = [
    path('tests/', views.lab_test_list_view, name='test_list'),
    path('tests/create/', views.lab_test_create_view, name='test_create'),
    path('tests/<int:pk>/update/', views.lab_test_update_view, name='test_update'),
    path('orders/', views.lab_order_list_view, name='order_list'),
    path('orders/create/', views.lab_order_create_view, name='order_create'),
    path('orders/<int:pk>/', views.lab_order_detail_view, name='order_detail'),
    path('orders/<int:pk>/update/', views.lab_order_update_view, name='order_update'),
    path('orders/<int:pk>/print/', views.lab_report_print_view, name='report_print'),
    path('results/upload/<int:item_pk>/', views.lab_result_upload_view, name='result_upload'),
    path('results/<int:pk>/', views.lab_result_detail_view, name='result_detail'),
    path('results/<int:pk>/download/', views.lab_report_download_view, name='result_download'),
]
