from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from hospitals.models import Branch
from .models import Department, Specialization
from .forms import DepartmentForm, SpecializationForm


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('branch', 'head')
        branch_id = self.request.GET.get('branch')
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Departments'
        context['table_id'] = 'departmentTable'
        context['create_url'] = reverse_lazy('departments:department_create')
        context['create_text'] = 'Add Department'
        context['branches'] = Branch.objects.all()
        return context


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('departments:department_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Department created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Department'
        context['cancel_url'] = reverse_lazy('departments:department_list')
        return context


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('departments:department_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Department updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Department'
        context['cancel_url'] = reverse_lazy('departments:department_list')
        return context


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('departments:department_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('departments:department_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Department deleted successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Department'
        context['cancel_url'] = reverse_lazy('departments:department_list')
        return context


class SpecializationListView(LoginRequiredMixin, ListView):
    model = Specialization
    template_name = 'departments/specialization_list.html'
    context_object_name = 'specializations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('department')
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Specializations'
        context['table_id'] = 'specializationTable'
        context['create_url'] = reverse_lazy('departments:specialization_create')
        context['create_text'] = 'Add Specialization'
        context['departments'] = Department.objects.all()
        return context


class SpecializationCreateView(LoginRequiredMixin, CreateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'departments/specialization_form.html'
    success_url = reverse_lazy('departments:specialization_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('departments:specialization_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Specialization created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Specialization'
        context['cancel_url'] = reverse_lazy('departments:specialization_list')
        return context


class SpecializationUpdateView(LoginRequiredMixin, UpdateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'departments/specialization_form.html'
    success_url = reverse_lazy('departments:specialization_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('departments:specialization_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Specialization updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Specialization'
        context['cancel_url'] = reverse_lazy('departments:specialization_list')
        return context


class SpecializationDeleteView(LoginRequiredMixin, DeleteView):
    model = Specialization
    template_name = 'departments/specialization_confirm_delete.html'
    success_url = reverse_lazy('departments:specialization_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('departments:specialization_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Specialization deleted successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Specialization'
        context['cancel_url'] = reverse_lazy('departments:specialization_list')
        return context
