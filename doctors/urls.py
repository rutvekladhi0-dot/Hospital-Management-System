from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('<int:pk>/update/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    path('schedules/', views.DoctorScheduleListView.as_view(), name='schedule_list'),
    path('schedules/create/', views.DoctorScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>/update/', views.DoctorScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/<int:pk>/delete/', views.DoctorScheduleDeleteView.as_view(), name='schedule_delete'),
    path('availability/', views.DoctorAvailabilityListView.as_view(), name='availability_list'),
    path('availability/create/', views.DoctorAvailabilityCreateView.as_view(), name='availability_create'),
    path('availability/<int:pk>/update/', views.DoctorAvailabilityUpdateView.as_view(), name='availability_update'),
    path('availability/<int:pk>/delete/', views.DoctorAvailabilityDeleteView.as_view(), name='availability_delete'),
]
