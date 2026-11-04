from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/mark/', views.AttendanceMarkView.as_view(), name='attendance_mark'),
    path('leaves/', views.LeaveListView.as_view(), name='leave_list'),
    path('leaves/apply/', views.LeaveCreateView.as_view(), name='leave_create'),
    path('leaves/<int:pk>/approve/', views.LeaveApproveView.as_view(), name='leave_approve'),
]
