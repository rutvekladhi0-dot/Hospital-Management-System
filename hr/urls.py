from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('designations/', views.designation_list_view, name='designation_list'),
    path('designations/create/', views.designation_create_view, name='designation_create'),
    path('records/', views.hr_record_list_view, name='hr_record_list'),
    path('records/create/', views.hr_record_create_view, name='hr_record_create'),
    path('trainings/', views.training_list_view, name='training_list'),
    path('trainings/create/', views.training_create_view, name='training_create'),
    path('trainings/<int:pk>/update/', views.training_update_view, name='training_update'),
]
