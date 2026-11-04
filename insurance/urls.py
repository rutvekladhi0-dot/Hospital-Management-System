from django.urls import path
from . import views

app_name = 'insurance'

urlpatterns = [
    path('providers/', views.provider_list_view, name='provider_list'),
    path('providers/create/', views.provider_create_view, name='provider_create'),
    path('providers/<int:pk>/update/', views.provider_update_view, name='provider_update'),
    path('plans/', views.plan_list_view, name='plan_list'),
    path('plans/create/', views.plan_create_view, name='plan_create'),
    path('plans/<int:pk>/update/', views.plan_update_view, name='plan_update'),
    path('patient-insurances/', views.patient_insurance_list_view, name='patient_insurance_list'),
    path('patient-insurances/create/', views.patient_insurance_create_view, name='patient_insurance_create'),
]
