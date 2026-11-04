from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department_list'),
    path('create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('specializations/', views.SpecializationListView.as_view(), name='specialization_list'),
    path('specializations/create/', views.SpecializationCreateView.as_view(), name='specialization_create'),
    path('specializations/<int:pk>/update/', views.SpecializationUpdateView.as_view(), name='specialization_update'),
    path('specializations/<int:pk>/delete/', views.SpecializationDeleteView.as_view(), name='specialization_delete'),
]
