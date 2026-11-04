from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.mixins import AdminRequiredMixin
from .models import Doctor, DoctorSchedule, DoctorAvailability
from .forms import DoctorForm, DoctorScheduleForm, DoctorAvailabilityForm


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'doctorTable'
        context['page_title'] = 'Doctors'
        return context


class DoctorCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctors:doctor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Doctor created successfully.')
        return super().form_valid(form)


class DoctorUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctors:doctor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Doctor updated successfully.')
        return super().form_valid(form)


class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'doctors/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedules'] = self.object.schedules.filter(is_active=True)
        context['availabilities'] = self.object.availabilities.filter(is_available=True)
        return context


class DoctorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctors:doctor_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Doctor deleted successfully.')
        return super().delete(request, *args, **kwargs)


class DoctorScheduleListView(LoginRequiredMixin, ListView):
    model = DoctorSchedule
    template_name = 'doctors/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('doctor__employee__user')
        doctor_id = self.request.GET.get('doctor')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'scheduleTable'
        context['page_title'] = 'Doctor Schedules'
        context['doctors'] = Doctor.objects.select_related('employee__user').all()
        return context


class DoctorScheduleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = DoctorSchedule
    form_class = DoctorScheduleForm
    template_name = 'doctors/schedule_form.html'
    success_url = reverse_lazy('doctors:schedule_list')

    def form_valid(self, form):
        messages.success(self.request, 'Schedule created successfully.')
        return super().form_valid(form)


class DoctorScheduleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = DoctorSchedule
    form_class = DoctorScheduleForm
    template_name = 'doctors/schedule_form.html'
    success_url = reverse_lazy('doctors:schedule_list')

    def form_valid(self, form):
        messages.success(self.request, 'Schedule updated successfully.')
        return super().form_valid(form)


class DoctorScheduleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = DoctorSchedule
    template_name = 'doctors/schedule_delete.html'
    success_url = reverse_lazy('doctors:schedule_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Schedule deleted successfully.')
        return super().delete(request, *args, **kwargs)


class DoctorAvailabilityListView(LoginRequiredMixin, ListView):
    model = DoctorAvailability
    template_name = 'doctors/availability_list.html'
    context_object_name = 'availabilities'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('doctor__employee__user')
        doctor_id = self.request.GET.get('doctor')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'availabilityTable'
        context['page_title'] = 'Doctor Availability'
        context['doctors'] = Doctor.objects.select_related('employee__user').all()
        return context


class DoctorAvailabilityCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = DoctorAvailability
    form_class = DoctorAvailabilityForm
    template_name = 'doctors/availability_form.html'
    success_url = reverse_lazy('doctors:availability_list')

    def form_valid(self, form):
        messages.success(self.request, 'Availability created successfully.')
        return super().form_valid(form)


class DoctorAvailabilityUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = DoctorAvailability
    form_class = DoctorAvailabilityForm
    template_name = 'doctors/availability_form.html'
    success_url = reverse_lazy('doctors:availability_list')

    def form_valid(self, form):
        messages.success(self.request, 'Availability updated successfully.')
        return super().form_valid(form)


class DoctorAvailabilityDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = DoctorAvailability
    template_name = 'doctors/availability_delete.html'
    success_url = reverse_lazy('doctors:availability_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Availability deleted successfully.')
        return super().delete(request, *args, **kwargs)
