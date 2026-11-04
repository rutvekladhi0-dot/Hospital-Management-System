from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='patient_list'),
    path('create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/update/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('records/', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('records/create/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('records/<int:pk>/update/', views.MedicalRecordUpdateView.as_view(), name='medical_record_update'),
    path('<int:patient_pk>/documents/', views.PatientDocumentListView.as_view(), name='patient_documents'),
    path('<int:patient_pk>/documents/upload/', views.PatientDocumentCreateView.as_view(), name='patient_document_upload'),
    path('documents/<int:pk>/delete/', views.PatientDocumentDeleteView.as_view(), name='patient_document_delete'),
]
