from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import Ambulance, AmbulanceRequest
from .forms import AmbulanceForm, AmbulanceRequestForm
from core.mixins import AdminRequiredMixin


class AmbulanceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Ambulance
    template_name = 'ambulance/ambulance_list.html'
    context_object_name = 'ambulances'
    paginate_by = 25

    def get_queryset(self):
        queryset = Ambulance.objects.all()
        search = self.request.GET.get('search')
        vehicle_type = self.request.GET.get('vehicle_type')

        if search:
            queryset = queryset.filter(
                Q(vehicle_number__icontains=search) |
                Q(driver_name__icontains=search)
            )
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'ambulanceTable'
        context['vehicle_types'] = Ambulance.VEHICLE_TYPE_CHOICES
        context['available_count'] = Ambulance.objects.filter(is_available=True).count()
        context['busy_count'] = Ambulance.objects.filter(is_available=False).count()
        return context


ambulance_list_view = AmbulanceListView.as_view()


class AmbulanceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Ambulance
    form_class = AmbulanceForm
    template_name = 'ambulance/ambulance_form.html'
    success_url = reverse_lazy('ambulance:ambulance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ambulance added successfully.')
        return super().form_valid(form)


ambulance_create_view = AmbulanceCreateView.as_view()


class AmbulanceUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Ambulance
    form_class = AmbulanceForm
    template_name = 'ambulance/ambulance_form.html'
    success_url = reverse_lazy('ambulance:ambulance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ambulance updated successfully.')
        return super().form_valid(form)


ambulance_update_view = AmbulanceUpdateView.as_view()


class RequestListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AmbulanceRequest
    template_name = 'ambulance/request_list.html'
    context_object_name = 'requests'
    paginate_by = 25

    def get_queryset(self):
        queryset = AmbulanceRequest.objects.select_related('ambulance', 'requested_by')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(patient_name__icontains=search) |
                Q(patient_phone__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'requestTable'
        context['status_choices'] = AmbulanceRequest.STATUS_CHOICES
        context['pending_count'] = AmbulanceRequest.objects.filter(status='Pending').count()
        context['active_count'] = AmbulanceRequest.objects.filter(status__in=['Dispatched', 'In-Transit']).count()
        return context


request_list_view = RequestListView.as_view()


class RequestCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AmbulanceRequest
    form_class = AmbulanceRequestForm
    template_name = 'ambulance/request_form.html'
    success_url = reverse_lazy('ambulance:request_list')

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        messages.success(self.request, 'Ambulance request created successfully.')
        return super().form_valid(form)


request_create_view = RequestCreateView.as_view()


class RequestUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = AmbulanceRequest
    form_class = AmbulanceRequestForm
    template_name = 'ambulance/request_form.html'
    success_url = reverse_lazy('ambulance:request_list')

    def form_valid(self, form):
        if form.instance.status == 'Dispatched' and self.object.status != 'Dispatched':
            form.instance.dispatched_at = timezone.now()
            if form.instance.ambulance:
                form.instance.ambulance.is_available = False
                form.instance.ambulance.save()
        elif form.instance.status in ('Completed', 'Cancelled') and self.object.status not in ('Completed', 'Cancelled'):
            form.instance.completed_at = timezone.now()
            if form.instance.ambulance:
                form.instance.ambulance.is_available = True
                form.instance.ambulance.save()
        messages.success(self.request, 'Request updated successfully.')
        return super().form_valid(form)


request_update_view = RequestUpdateView.as_view()


class RequestDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = AmbulanceRequest
    template_name = 'ambulance/request_detail.html'
    context_object_name = 'ambulance_request'


request_detail_view = RequestDetailView.as_view()
