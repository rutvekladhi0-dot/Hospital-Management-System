from django.urls import path
from . import views

app_name = 'ipd'

urlpatterns = [
    path('wards/', views.ward_list_view, name='ward_list'),
    path('wards/create/', views.ward_create_view, name='ward_create'),
    path('wards/<int:pk>/update/', views.ward_update_view, name='ward_update'),
    path('beds/', views.bed_list_view, name='bed_list'),
    path('admissions/', views.admission_list_view, name='admission_list'),
    path('admissions/create/', views.admission_create_view, name='admission_create'),
    path('admissions/<int:pk>/', views.admission_detail_view, name='admission_detail'),
    path('admissions/<int:pk>/discharge/', views.discharge_view, name='discharge'),
    path('admissions/<int:pk>/transfer/', views.bed_transfer_view, name='bed_transfer'),
]
