from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Count

from .models import Designation, HRRecord, Training
from .forms import DesignationForm, HRRecordForm, TrainingForm
from core.mixins import HRManagerRequiredMixin


class DesignationListView(LoginRequiredMixin, HRManagerRequiredMixin, ListView):
    model = Designation
    template_name = 'hr/designation_list.html'
    context_object_name = 'designations'
    paginate_by = 25

    def get_queryset(self):
        queryset = Designation.objects.select_related('department')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'designationTable'
        return context


designation_list_view = DesignationListView.as_view()


class DesignationCreateView(LoginRequiredMixin, HRManagerRequiredMixin, CreateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'hr/designation_form.html'
    success_url = reverse_lazy('hr:designation_list')

    def form_valid(self, form):
        messages.success(self.request, 'Designation created successfully.')
        return super().form_valid(form)


designation_create_view = DesignationCreateView.as_view()


class HRRecordListView(LoginRequiredMixin, HRManagerRequiredMixin, ListView):
    model = HRRecord
    template_name = 'hr/hr_record_list.html'
    context_object_name = 'records'
    paginate_by = 25

    def get_queryset(self):
        queryset = HRRecord.objects.select_related('employee__user', 'created_by')
        search = self.request.GET.get('search')
        record_type = self.request.GET.get('record_type')

        if search:
            queryset = queryset.filter(
                Q(employee__employee_id__icontains=search) |
                Q(employee__user__first_name__icontains=search) |
                Q(employee__user__last_name__icontains=search)
            )
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'hrRecordTable'
        context['record_types'] = HRRecord.RECORD_TYPE_CHOICES
        return context


hr_record_list_view = HRRecordListView.as_view()


class HRRecordCreateView(LoginRequiredMixin, HRManagerRequiredMixin, CreateView):
    model = HRRecord
    form_class = HRRecordForm
    template_name = 'hr/hr_record_form.html'
    success_url = reverse_lazy('hr:hr_record_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'HR record created successfully.')
        return super().form_valid(form)


hr_record_create_view = HRRecordCreateView.as_view()


class TrainingListView(LoginRequiredMixin, HRManagerRequiredMixin, ListView):
    model = Training
    template_name = 'hr/training_list.html'
    context_object_name = 'trainings'
    paginate_by = 25

    def get_queryset(self):
        queryset = Training.objects.annotate(participant_count=Count('employees')).order_by('-start_date')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(trainer__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'trainingTable'
        context['status_choices'] = Training.STATUS_CHOICES
        return context


training_list_view = TrainingListView.as_view()


class TrainingCreateView(LoginRequiredMixin, HRManagerRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = 'hr/training_form.html'
    success_url = reverse_lazy('hr:training_list')

    def form_valid(self, form):
        messages.success(self.request, 'Training created successfully.')
        return super().form_valid(form)


training_create_view = TrainingCreateView.as_view()


class TrainingUpdateView(LoginRequiredMixin, HRManagerRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = 'hr/training_form.html'
    success_url = reverse_lazy('hr:training_list')

    def form_valid(self, form):
        messages.success(self.request, 'Training updated successfully.')
        return super().form_valid(form)


training_update_view = TrainingUpdateView.as_view()
