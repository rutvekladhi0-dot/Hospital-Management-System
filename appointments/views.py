from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from core.mixins import AdminRequiredMixin, DoctorRequiredMixin, ReceptionistRequiredMixin, PatientRequiredMixin, AppointmentViewMixin
from .models import Appointment, Visit
from .forms import AppointmentForm, AppointmentUpdateForm, VisitForm


class AppointmentListView(LoginRequiredMixin, AppointmentViewMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            'patient__user', 'doctor__employee__user', 'department'
        )
        user = self.request.user
        if user.is_patient:
            qs = qs.filter(patient__user=user)
        elif user.is_doctor:
            qs = qs.filter(doctor__employee__user=user)
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        apt_type = self.request.GET.get('type')
        if apt_type:
            qs = qs.filter(appointment_type=apt_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'appointmentTable'
        context['page_title'] = 'Appointments'
        return context


class AppointmentCreateView(LoginRequiredMixin, AppointmentViewMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:appointment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment booked successfully.')
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, AppointmentViewMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:appointment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment updated successfully.')
        return super().form_valid(form)


class AppointmentDetailView(LoginRequiredMixin, AppointmentViewMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visit'] = Visit.objects.filter(appointment=self.object).first()
        return context


class AppointmentCancelView(LoginRequiredMixin, AppointmentViewMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointments:appointment_list')


class AppointmentConfirmView(LoginRequiredMixin, AppointmentViewMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = 'Confirmed'
        appointment.save()
        messages.success(request, 'Appointment confirmed successfully.')
        return redirect('appointments:appointment_list')


class AppointmentCheckinView(LoginRequiredMixin, AppointmentViewMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = 'In-Progress'
        appointment.save()
        messages.success(request, 'Patient checked in successfully.')
        return redirect('appointments:appointment_list')


class AppointmentCompleteView(LoginRequiredMixin, DoctorRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = 'Completed'
        appointment.save()
        messages.success(request, 'Appointment marked as completed.')
        return redirect('appointments:appointment_list')


class VisitCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = Visit
    form_class = VisitForm
    template_name = 'appointments/visit_form.html'
    success_url = reverse_lazy('appointments:appointment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Visit record created successfully.')
        return super().form_valid(form)


class VisitDetailView(LoginRequiredMixin, DoctorRequiredMixin, DetailView):
    model = Visit
    template_name = 'appointments/visit_detail.html'
    context_object_name = 'visit'
