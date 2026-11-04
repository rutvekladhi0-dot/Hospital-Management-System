from django.urls import path
from . import views

app_name = 'opd'

urlpatterns = [
    path('', views.opd_list_view, name='opd_list'),
    path('create/', views.opd_create_view, name='opd_create'),
    path('<int:pk>/', views.opd_detail_view, name='opd_detail'),
    path('<int:pk>/update/', views.opd_update_view, name='opd_update'),
    path('<int:pk>/complete/', views.opd_complete_view, name='opd_complete'),
]
