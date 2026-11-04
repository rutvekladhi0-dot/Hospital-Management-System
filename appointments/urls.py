from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('<int:pk>/cancel/', views.AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('<int:pk>/confirm/', views.AppointmentConfirmView.as_view(), name='appointment_confirm'),
    path('<int:pk>/checkin/', views.AppointmentCheckinView.as_view(), name='appointment_checkin'),
    path('<int:pk>/complete/', views.AppointmentCompleteView.as_view(), name='appointment_complete'),
    path('visits/create/', views.VisitCreateView.as_view(), name='visit_create'),
    path('visits/<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
]
