from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Employee, Attendance, LeaveRequest
from .forms import EmployeeForm, AttendanceForm, LeaveRequestForm, LeaveApprovalForm
from core.mixins import HRManagerRequiredMixin


class EmployeeListView(LoginRequiredMixin, HRManagerRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user', 'department')
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(user__first_name__icontains=search) |
                models.Q(user__last_name__icontains=search) |
                models.Q(employee_id__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employees'
        context['table_id'] = 'employeeTable'
        context['create_url'] = reverse_lazy('employees:employee_create')
        context['create_text'] = 'Add Employee'
        from departments.models import Department
        context['departments'] = Department.objects.all()
        return context


class EmployeeCreateView(LoginRequiredMixin, HRManagerRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('employees:employee_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Employee created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Employee'
        context['cancel_url'] = reverse_lazy('employees:employee_list')
        return context


class EmployeeUpdateView(LoginRequiredMixin, HRManagerRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('employees:employee_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Employee updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Employee'
        context['cancel_url'] = reverse_lazy('employees:employee_list')
        return context


class EmployeeDetailView(LoginRequiredMixin, HRManagerRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Detail'
        context['attendances'] = self.object.attendances.all()[:10]
        context['leave_requests'] = self.object.leave_requests.all()[:10]
        return context


class EmployeeDeleteView(LoginRequiredMixin, HRManagerRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employees:employee_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('employees:employee_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Employee deleted successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Employee'
        context['cancel_url'] = reverse_lazy('employees:employee_list')
        return context


class AttendanceListView(LoginRequiredMixin, HRManagerRequiredMixin, ListView):
    model = Attendance
    template_name = 'employees/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('employee__user')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Attendance'
        context['table_id'] = 'attendanceTable'
        context['create_url'] = reverse_lazy('employees:attendance_mark')
        context['create_text'] = 'Mark Attendance'
        return context


class AttendanceMarkView(LoginRequiredMixin, HRManagerRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('employees:attendance_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('employees:attendance_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Attendance marked successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mark Attendance'
        context['cancel_url'] = reverse_lazy('employees:attendance_list')
        return context


class LeaveListView(LoginRequiredMixin, HRManagerRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'employees/leave_list.html'
    context_object_name = 'leave_requests'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('employee__user')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            try:
                emp = Employee.objects.get(user=self.request.user)
                queryset = queryset.filter(employee=emp)
            except Employee.DoesNotExist:
                queryset = LeaveRequest.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Leave Requests'
        context['table_id'] = 'leaveTable'
        context['create_url'] = reverse_lazy('employees:leave_create')
        context['create_text'] = 'Apply for Leave'
        context['is_staff'] = self.request.user.is_staff or self.request.user.is_superuser
        return context


class LeaveCreateView(LoginRequiredMixin, HRManagerRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'employees/leave_form.html'
    success_url = reverse_lazy('employees:leave_list')

    def form_valid(self, form):
        messages.success(self.request, 'Leave request submitted successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Apply for Leave'
        context['cancel_url'] = reverse_lazy('employees:leave_list')
        return context


class LeaveApproveView(LoginRequiredMixin, HRManagerRequiredMixin, DetailView):
    model = LeaveRequest
    template_name = 'employees/leave_approve.html'
    context_object_name = 'leave_request'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('employees:leave_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        leave_request = self.get_object()
        form = LeaveApprovalForm(request.POST)
        if form.is_valid():
            leave_request.status = form.cleaned_data['status']
            leave_request.approved_by = request.user
            leave_request.save()
            messages.success(request, f'Leave request {leave_request.status.lower()} successfully.')
            return redirect('employees:leave_list')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Approve Leave Request'
        context['form'] = LeaveApprovalForm()
        context['cancel_url'] = reverse_lazy('employees:leave_list')
        return context
