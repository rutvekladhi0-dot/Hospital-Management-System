from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_dashboard_view, name='report_dashboard'),
    path('revenue/', views.revenue_report_view, name='revenue_report'),
    path('revenue/export/pdf/', views.export_revenue_pdf_view, name='export_revenue_pdf'),
    path('revenue/export/excel/', views.export_revenue_excel_view, name='export_revenue_excel'),
    path('revenue/export/csv/', views.export_revenue_csv_view, name='export_revenue_csv'),
    path('appointments/', views.appointment_report_view, name='appointment_report'),
    path('appointments/export/pdf/', views.export_appointment_pdf_view, name='export_appointment_pdf'),
    path('appointments/export/excel/', views.export_appointment_excel_view, name='export_appointment_excel'),
    path('appointments/export/csv/', views.export_appointment_csv_view, name='export_appointment_csv'),
    path('patients/', views.patient_report_view, name='patient_report'),
    path('patients/export/pdf/', views.export_patient_pdf_view, name='export_patient_pdf'),
    path('patients/export/excel/', views.export_patient_excel_view, name='export_patient_excel'),
    path('patients/export/csv/', views.export_patient_csv_view, name='export_patient_csv'),
    path('pharmacy/', views.pharmacy_report_view, name='pharmacy_report'),
    path('pharmacy/export/pdf/', views.export_pharmacy_pdf_view, name='export_pharmacy_pdf'),
    path('pharmacy/export/excel/', views.export_pharmacy_excel_view, name='export_pharmacy_excel'),
    path('pharmacy/export/csv/', views.export_pharmacy_csv_view, name='export_pharmacy_csv'),
    path('inventory/', views.inventory_report_view, name='inventory_report'),
    path('inventory/export/pdf/', views.export_inventory_pdf_view, name='export_inventory_pdf'),
    path('inventory/export/excel/', views.export_inventory_excel_view, name='export_inventory_excel'),
    path('inventory/export/csv/', views.export_inventory_csv_view, name='export_inventory_csv'),
    path('lab/', views.lab_report_view, name='lab_report'),
    path('lab/export/pdf/', views.export_lab_pdf_view, name='export_lab_pdf'),
    path('lab/export/excel/', views.export_lab_excel_view, name='export_lab_excel'),
    path('lab/export/csv/', views.export_lab_csv_view, name='export_lab_csv'),
    path('employees/', views.employee_report_view, name='employee_report'),
    path('employees/export/pdf/', views.export_employee_pdf_view, name='export_employee_pdf'),
    path('employees/export/excel/', views.export_employee_excel_view, name='export_employee_excel'),
    path('employees/export/csv/', views.export_employee_csv_view, name='export_employee_csv'),
]
