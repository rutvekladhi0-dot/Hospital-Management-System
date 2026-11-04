from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import Ward, Bed, Admission, BedTransfer
from .forms import WardForm, BedForm, AdmissionForm, DischargeForm, BedTransferForm
from core.mixins import AdminRequiredMixin, NurseOrAdminRequiredMixin


class WardListView(LoginRequiredMixin, NurseOrAdminRequiredMixin, ListView):
    model = Ward
    template_name = 'ipd/ward_list.html'
    context_object_name = 'wards'
    paginate_by = 25

    def get_queryset(self):
        queryset = Ward.objects.select_related('department')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(department__name__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'wardTable'
        return context


ward_list_view = WardListView.as_view()


class WardCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Ward
    form_class = WardForm
    template_name = 'ipd/ward_form.html'
    success_url = reverse_lazy('ipd:ward_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ward created successfully.')
        return super().form_valid(form)


ward_create_view = WardCreateView.as_view()


class WardUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Ward
    form_class = WardForm
    template_name = 'ipd/ward_form.html'
    success_url = reverse_lazy('ipd:ward_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ward updated successfully.')
        return super().form_valid(form)


ward_update_view = WardUpdateView.as_view()


class BedListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Bed
    template_name = 'ipd/bed_list.html'
    context_object_name = 'beds'
    paginate_by = 25

    def get_queryset(self):
        queryset = Bed.objects.select_related('ward')
        search = self.request.GET.get('search')
        ward = self.request.GET.get('ward')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(bed_number__icontains=search) |
                Q(ward__name__icontains=search)
            )
        if ward:
            queryset = queryset.filter(ward_id=ward)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'bedTable'
        context['wards'] = Ward.objects.filter(is_active=True)
        context['available_beds'] = Bed.objects.filter(status='Available').count()
        context['occupied_beds'] = Bed.objects.filter(status='Occupied').count()
        context['reserved_beds'] = Bed.objects.filter(status='Reserved').count()
        return context


bed_list_view = BedListView.as_view()


class AdmissionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Admission
    template_name = 'ipd/admission_list.html'
    context_object_name = 'admissions'
    paginate_by = 25

    def get_queryset(self):
        queryset = Admission.objects.select_related('patient', 'doctor', 'doctor__employee', 'doctor__employee__user', 'ward', 'bed')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(patient__patient_id__icontains=search) |
                Q(patient__user__first_name__icontains=search) |
                Q(patient__user__last_name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        else:
            queryset = queryset.filter(status='Admitted')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'admissionTable'
        context['total_admitted'] = Admission.objects.filter(status='Admitted').count()
        context['total_discharged'] = Admission.objects.filter(status='Discharged').count()
        return context


admission_list_view = AdmissionListView.as_view()


class AdmissionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Admission
    form_class = AdmissionForm
    template_name = 'ipd/admission_form.html'
    success_url = reverse_lazy('ipd:admission_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient admitted successfully.')
        return super().form_valid(form)


admission_create_view = AdmissionCreateView.as_view()


class AdmissionDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Admission
    template_name = 'ipd/admission_detail.html'
    context_object_name = 'admission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transfers'] = self.object.bed_transfers.all()
        context['discharge_form'] = DischargeForm()
        context['transfer_form'] = BedTransferForm()
        return context


admission_detail_view = AdmissionDetailView.as_view()


class DischargeView(LoginRequiredMixin, AdminRequiredMixin, FormView):
    form_class = DischargeForm
    template_name = 'ipd/discharge_form.html'

    def form_valid(self, form):
        admission = get_object_or_404(Admission, pk=self.kwargs['pk'])
        admission.status = 'Discharged'
        admission.discharge_date = timezone.now()
        admission.discharge_notes = form.cleaned_data.get('discharge_notes', '')
        admission.bed.status = 'Available'
        admission.bed.save()
        admission.save()
        messages.success(self.request, 'Patient discharged successfully.')
        return redirect('ipd:admission_list')


discharge_view = DischargeView.as_view()


class BedTransferView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = BedTransfer
    form_class = BedTransferForm
    template_name = 'ipd/bed_transfer_form.html'

    def form_valid(self, form):
        admission = get_object_or_404(Admission, pk=self.kwargs['pk'])
        transfer = form.save(commit=False)
        transfer.admission = admission
        transfer.from_ward = admission.ward
        transfer.from_bed = admission.bed
        transfer.transferred_by = self.request.user
        transfer.save()
        messages.success(self.request, 'Bed transfer completed successfully.')
        return redirect('ipd:admission_detail', pk=admission.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admission'] = get_object_or_404(Admission, pk=self.kwargs['pk'])
        return context


bed_transfer_view = BedTransferView.as_view()
