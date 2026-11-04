from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list_view, name='notification_list'),
    path('api/', views.notification_api_view, name='notification_api'),
    path('<int:pk>/read/', views.notification_mark_read_view, name='notification_mark_read'),
    path('mark-all-read/', views.notification_mark_all_read_view, name='notification_mark_all_read'),
    path('<int:pk>/delete/', views.notification_delete_view, name='notification_delete'),
]
