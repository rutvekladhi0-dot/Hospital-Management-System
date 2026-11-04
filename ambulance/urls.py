from django.urls import path
from . import views

app_name = 'ambulance'

urlpatterns = [
    path('ambulances/', views.ambulance_list_view, name='ambulance_list'),
    path('ambulances/create/', views.ambulance_create_view, name='ambulance_create'),
    path('ambulances/<int:pk>/update/', views.ambulance_update_view, name='ambulance_update'),
    path('requests/', views.request_list_view, name='request_list'),
    path('requests/create/', views.request_create_view, name='request_create'),
    path('requests/<int:pk>/update/', views.request_update_view, name='request_update'),
    path('requests/<int:pk>/', views.request_detail_view, name='request_detail'),
]
