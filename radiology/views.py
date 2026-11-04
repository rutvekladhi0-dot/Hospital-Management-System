from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

from .models import RadiologyTest, RadiologyOrder, RadiologyReport
from .forms import RadiologyTestForm, RadiologyOrderForm, RadiologyReportForm
from core.mixins import LabTechnicianRequiredMixin, DoctorOrLabTechnicianRequiredMixin


class RadiologyTestListView(LoginRequiredMixin, LabTechnicianRequiredMixin, ListView):
    model = RadiologyTest
    template_name = 'radiology/radiology_test_list.html'
    context_object_name = 'tests'
    paginate_by = 25

    def get_queryset(self):
        queryset = RadiologyTest.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'radiologyTestTable'
        return context


class RadiologyTestCreateView(LoginRequiredMixin, LabTechnicianRequiredMixin, CreateView):
    model = RadiologyTest
    form_class = RadiologyTestForm
    template_name = 'radiology/radiology_test_form.html'
    success_url = reverse_lazy('radiology:test_list')

    def form_valid(self, form):
        messages.success(self.request, 'Radiology test created successfully.')
        return super().form_valid(form)


class RadiologyOrderListView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, ListView):
    model = RadiologyOrder
    template_name = 'radiology/radiology_order_list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_queryset(self):
        queryset = RadiologyOrder.objects.select_related('patient', 'doctor', 'test')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(test__name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'radiologyOrderTable'
        context['status_choices'] = RadiologyOrder.STATUS_CHOICES
        return context


class RadiologyOrderCreateView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, CreateView):
    model = RadiologyOrder
    form_class = RadiologyOrderForm
    template_name = 'radiology/radiology_order_form.html'
    success_url = reverse_lazy('radiology:order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Radiology order created successfully.')
        return super().form_valid(form)


class RadiologyOrderDetailView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, DetailView):
    model = RadiologyOrder
    template_name = 'radiology/radiology_order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report'] = RadiologyReport.objects.filter(order=self.object).first()
        return context


class RadiologyOrderUpdateView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, UpdateView):
    model = RadiologyOrder
    form_class = RadiologyOrderForm
    template_name = 'radiology/radiology_order_form.html'
    success_url = reverse_lazy('radiology:order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Radiology order updated successfully.')
        return super().form_valid(form)


class RadiologyReportUploadView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, CreateView):
    model = RadiologyReport
    form_class = RadiologyReportForm
    template_name = 'radiology/radiology_report_form.html'

    def form_valid(self, form):
        order = get_object_or_404(RadiologyOrder, pk=self.kwargs['order_pk'])
        form.instance.order = order
        form.instance.reported_by = self.request.user

        order.status = 'Completed'
        order.completed_at = timezone.now()
        order.save()

        messages.success(self.request, 'Radiology report uploaded successfully.')
        return redirect('radiology:order_detail', pk=order.pk)


class RadiologyReportDetailView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, DetailView):
    model = RadiologyReport
    template_name = 'radiology/radiology_report_detail.html'
    context_object_name = 'report'


@login_required
def appointments_by_patient_api(request):
    patient_id = request.GET.get('patient_id')
    if not patient_id:
        return JsonResponse([], safe=False)
    from appointments.models import Appointment
    appointments = Appointment.objects.filter(
        patient_id=patient_id
    ).select_related('doctor__employee__user').order_by('-appointment_date')
    data = [
        {
            'id': a.pk,
            'label': f"{a.appointment_date} - Dr. {a.doctor.employee.user.get_full_name()} ({a.get_appointment_type_display()})"
        }
        for a in appointments
    ]
    return JsonResponse(data, safe=False)


radiology_test_list_view = RadiologyTestListView.as_view()
radiology_test_create_view = RadiologyTestCreateView.as_view()
radiology_order_list_view = RadiologyOrderListView.as_view()
radiology_order_create_view = RadiologyOrderCreateView.as_view()
radiology_order_detail_view = RadiologyOrderDetailView.as_view()
radiology_order_update_view = RadiologyOrderUpdateView.as_view()
radiology_report_upload_view = RadiologyReportUploadView.as_view()
radiology_report_detail_view = RadiologyReportDetailView.as_view()
