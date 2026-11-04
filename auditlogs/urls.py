from django.urls import path
from . import views

app_name = 'auditlogs'

urlpatterns = [
    path('', views.audit_log_list_view, name='audit_log_list'),
    path('<int:pk>/', views.audit_log_detail_view, name='audit_log_detail'),
]
