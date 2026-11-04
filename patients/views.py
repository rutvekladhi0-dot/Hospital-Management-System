from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.mixins import AdminRequiredMixin, ReceptionistRequiredMixin, DoctorRequiredMixin
from .models import Patient, MedicalRecord, PatientDocument
from .forms import PatientForm, MedicalRecordForm, PatientDocumentForm


class PatientListView(LoginRequiredMixin, ReceptionistRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'patientTable'
        context['page_title'] = 'Patients'
        return context


class PatientCreateView(LoginRequiredMixin, ReceptionistRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:patient_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient registered successfully.')
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, ReceptionistRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:patient_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient updated successfully.')
        return super().form_valid(form)


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_records'] = self.object.medical_records.all()[:10]
        context['documents'] = self.object.documents.all()[:10]
        return context


class PatientDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patients:patient_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Patient deleted successfully.')
        return super().delete(request, *args, **kwargs)


class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'patients/medical_record_list.html'
    context_object_name = 'records'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('patient__user', 'doctor')
        patient_id = self.request.GET.get('patient')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        if self.request.user.is_patient:
            qs = qs.filter(patient__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'medicalRecordTable'
        context['page_title'] = 'Medical Records'
        return context


class MedicalRecordCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'patients/medical_record_form.html'
    success_url = reverse_lazy('patients:medical_record_list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        messages.success(self.request, 'Medical record created successfully.')
        return super().form_valid(form)


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'patients/medical_record_detail.html'
    context_object_name = 'record'


class MedicalRecordUpdateView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'patients/medical_record_form.html'
    success_url = reverse_lazy('patients:medical_record_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medical record updated successfully.')
        return super().form_valid(form)


class PatientDocumentListView(LoginRequiredMixin, ListView):
    model = PatientDocument
    template_name = 'patients/patient_document_list.html'
    context_object_name = 'documents'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('patient__user', 'uploaded_by')
        patient_pk = self.kwargs.get('patient_pk')
        if patient_pk:
            qs = qs.filter(patient_id=patient_pk)
        if self.request.user.is_patient:
            qs = qs.filter(patient__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs.get('patient_pk'))
        context['page_title'] = 'Patient Documents'
        return context


class PatientDocumentCreateView(LoginRequiredMixin, CreateView):
    model = PatientDocument
    form_class = PatientDocumentForm
    template_name = 'patients/patient_document_form.html'

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(Patient, pk=self.kwargs.get('patient_pk'))
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Document uploaded successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patients:patient_documents', kwargs={'patient_pk': self.kwargs.get('patient_pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs.get('patient_pk'))
        return context


class PatientDocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = PatientDocument
    template_name = 'patients/patient_document_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('patients:patient_documents', kwargs={'patient_pk': self.object.patient.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Document deleted successfully.')
        return super().delete(request, *args, **kwargs)
