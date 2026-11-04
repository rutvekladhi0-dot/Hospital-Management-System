from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import NursingStation, NursingTask, VitalSigns
from .forms import NursingStationForm, NursingTaskForm, VitalSignsForm
from core.mixins import NurseRequiredMixin


class StationListView(LoginRequiredMixin, NurseRequiredMixin, ListView):
    model = NursingStation
    template_name = 'nursing/station_list.html'
    context_object_name = 'stations'
    paginate_by = 25

    def get_queryset(self):
        return NursingStation.objects.select_related('ward', 'nurse_in_charge')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'stationTable'
        return context


station_list_view = StationListView.as_view()


class StationCreateView(LoginRequiredMixin, NurseRequiredMixin, CreateView):
    model = NursingStation
    form_class = NursingStationForm
    template_name = 'nursing/station_form.html'
    success_url = reverse_lazy('nursing:station_list')

    def form_valid(self, form):
        messages.success(self.request, 'Nursing station created successfully.')
        return super().form_valid(form)


station_create_view = StationCreateView.as_view()


class TaskListView(LoginRequiredMixin, NurseRequiredMixin, ListView):
    model = NursingTask
    template_name = 'nursing/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 25

    def get_queryset(self):
        queryset = NursingTask.objects.select_related('patient__user', 'assigned_to')
        status = self.request.GET.get('status')
        task_type = self.request.GET.get('task_type')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(assigned_to=self.request.user)

        if status:
            queryset = queryset.filter(status=status)
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'taskTable'
        context['status_choices'] = NursingTask.STATUS_CHOICES
        context['task_types'] = NursingTask.TASK_TYPE_CHOICES
        return context


task_list_view = TaskListView.as_view()


class TaskCreateView(LoginRequiredMixin, NurseRequiredMixin, CreateView):
    model = NursingTask
    form_class = NursingTaskForm
    template_name = 'nursing/task_form.html'
    success_url = reverse_lazy('nursing:task_list')

    def form_valid(self, form):
        messages.success(self.request, 'Nursing task created successfully.')
        return super().form_valid(form)


task_create_view = TaskCreateView.as_view()


class TaskUpdateView(LoginRequiredMixin, NurseRequiredMixin, UpdateView):
    model = NursingTask
    form_class = NursingTaskForm
    template_name = 'nursing/task_form.html'
    success_url = reverse_lazy('nursing:task_list')

    def form_valid(self, form):
        if form.instance.status == 'Completed' and self.object.status != 'Completed':
            form.instance.completed_at = timezone.now()
        messages.success(self.request, 'Nursing task updated successfully.')
        return super().form_valid(form)


task_update_view = TaskUpdateView.as_view()


class VitalsListView(LoginRequiredMixin, NurseRequiredMixin, ListView):
    model = VitalSigns
    template_name = 'nursing/vitals_list.html'
    context_object_name = 'vitals_list'
    paginate_by = 25

    def get_queryset(self):
        queryset = VitalSigns.objects.select_related('patient__user', 'recorded_by')
        patient_id = self.request.GET.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'vitalsTable'
        return context


vitals_list_view = VitalsListView.as_view()


class VitalsCreateView(LoginRequiredMixin, NurseRequiredMixin, CreateView):
    model = VitalSigns
    form_class = VitalSignsForm
    template_name = 'nursing/vitals_form.html'
    success_url = reverse_lazy('nursing:vitals_list')

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Vital signs recorded successfully.')
        return super().form_valid(form)


vitals_create_view = VitalsCreateView.as_view()
