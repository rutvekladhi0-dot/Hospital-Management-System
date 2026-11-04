from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import InsuranceProvider, InsurancePlan, PatientInsurance
from .forms import InsuranceProviderForm, InsurancePlanForm, PatientInsuranceForm
from core.mixins import ReceptionistRequiredMixin


class InsuranceProviderListView(LoginRequiredMixin, ReceptionistRequiredMixin, ListView):
    model = InsuranceProvider
    template_name = 'insurance/provider_list.html'
    context_object_name = 'providers'
    paginate_by = 25

    def get_queryset(self):
        queryset = InsuranceProvider.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(phone__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'providerTable'
        return context


provider_list_view = InsuranceProviderListView.as_view()


class InsuranceProviderCreateView(LoginRequiredMixin, ReceptionistRequiredMixin, CreateView):
    model = InsuranceProvider
    form_class = InsuranceProviderForm
    template_name = 'insurance/provider_form.html'
    success_url = reverse_lazy('insurance:provider_list')

    def form_valid(self, form):
        messages.success(self.request, 'Insurance provider created successfully.')
        return super().form_valid(form)


provider_create_view = InsuranceProviderCreateView.as_view()


class InsuranceProviderUpdateView(LoginRequiredMixin, ReceptionistRequiredMixin, UpdateView):
    model = InsuranceProvider
    form_class = InsuranceProviderForm
    template_name = 'insurance/provider_form.html'
    success_url = reverse_lazy('insurance:provider_list')

    def form_valid(self, form):
        messages.success(self.request, 'Insurance provider updated successfully.')
        return super().form_valid(form)


provider_update_view = InsuranceProviderUpdateView.as_view()


class InsurancePlanListView(LoginRequiredMixin, ReceptionistRequiredMixin, ListView):
    model = InsurancePlan
    template_name = 'insurance/plan_list.html'
    context_object_name = 'plans'
    paginate_by = 25

    def get_queryset(self):
        queryset = InsurancePlan.objects.select_related('provider')
        search = self.request.GET.get('search')
        provider = self.request.GET.get('provider')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(provider__name__icontains=search)
            )
        if provider:
            queryset = queryset.filter(provider_id=provider)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'planTable'
        context['providers'] = InsuranceProvider.objects.filter(is_active=True)
        return context


plan_list_view = InsurancePlanListView.as_view()


class InsurancePlanCreateView(LoginRequiredMixin, ReceptionistRequiredMixin, CreateView):
    model = InsurancePlan
    form_class = InsurancePlanForm
    template_name = 'insurance/plan_form.html'
    success_url = reverse_lazy('insurance:plan_list')

    def form_valid(self, form):
        messages.success(self.request, 'Insurance plan created successfully.')
        return super().form_valid(form)


plan_create_view = InsurancePlanCreateView.as_view()


class InsurancePlanUpdateView(LoginRequiredMixin, ReceptionistRequiredMixin, UpdateView):
    model = InsurancePlan
    form_class = InsurancePlanForm
    template_name = 'insurance/plan_form.html'
    success_url = reverse_lazy('insurance:plan_list')

    def form_valid(self, form):
        messages.success(self.request, 'Insurance plan updated successfully.')
        return super().form_valid(form)


plan_update_view = InsurancePlanUpdateView.as_view()


class PatientInsuranceListView(LoginRequiredMixin, ReceptionistRequiredMixin, ListView):
    model = PatientInsurance
    template_name = 'insurance/patient_insurance_list.html'
    context_object_name = 'patient_insurances'
    paginate_by = 25

    def get_queryset(self):
        queryset = PatientInsurance.objects.select_related('patient', 'plan', 'plan__provider')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient__patient_id__icontains=search) |
                Q(patient__user__first_name__icontains=search) |
                Q(patient__user__last_name__icontains=search) |
                Q(policy_number__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'patientInsuranceTable'
        return context


patient_insurance_list_view = PatientInsuranceListView.as_view()


class PatientInsuranceCreateView(LoginRequiredMixin, ReceptionistRequiredMixin, CreateView):
    model = PatientInsurance
    form_class = PatientInsuranceForm
    template_name = 'insurance/patient_insurance_form.html'
    success_url = reverse_lazy('insurance:patient_insurance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient insurance added successfully.')
        return super().form_valid(form)


patient_insurance_create_view = PatientInsuranceCreateView.as_view()
