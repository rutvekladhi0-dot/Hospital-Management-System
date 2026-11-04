from django.urls import path
from . import views

app_name = 'nursing'

urlpatterns = [
    path('stations/', views.station_list_view, name='station_list'),
    path('stations/create/', views.station_create_view, name='station_create'),
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update_view, name='task_update'),
    path('vitals/', views.vitals_list_view, name='vitals_list'),
    path('vitals/create/', views.vitals_create_view, name='vitals_create'),
]
