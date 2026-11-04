from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.http import FileResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import LabTest, LabOrder, LabOrderItem, LabResult
from .forms import LabTestForm, LabOrderForm, LabOrderItemForm, LabResultForm
from core.mixins import LabTechnicianRequiredMixin, DoctorOrLabTechnicianRequiredMixin, DoctorLabOrPatientRequiredMixin


class LabTestListView(LoginRequiredMixin, LabTechnicianRequiredMixin, ListView):
    model = LabTest
    template_name = 'laboratory/lab_test_list.html'
    context_object_name = 'tests'
    paginate_by = 25

    def get_queryset(self):
        queryset = LabTest.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'labTestTable'
        return context


class LabTestCreateView(LoginRequiredMixin, LabTechnicianRequiredMixin, CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/lab_test_form.html'
    success_url = reverse_lazy('laboratory:test_list')

    def form_valid(self, form):
        messages.success(self.request, 'Lab test created successfully.')
        return super().form_valid(form)


class LabTestUpdateView(LoginRequiredMixin, LabTechnicianRequiredMixin, UpdateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/lab_test_form.html'
    success_url = reverse_lazy('laboratory:test_list')

    def form_valid(self, form):
        messages.success(self.request, 'Lab test updated successfully.')
        return super().form_valid(form)


class LabOrderListView(LoginRequiredMixin, DoctorLabOrPatientRequiredMixin, ListView):
    model = LabOrder
    template_name = 'laboratory/lab_order_list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_queryset(self):
        queryset = LabOrder.objects.select_related('patient', 'doctor')
        if self.request.user.is_patient:
            queryset = queryset.filter(patient__user=self.request.user)
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'labOrderTable'
        context['status_choices'] = LabOrder.STATUS_CHOICES
        return context


class LabOrderCreateView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, CreateView):
    model = LabOrder
    form_class = LabOrderForm
    template_name = 'laboratory/lab_order_form.html'
    success_url = reverse_lazy('laboratory:order_list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        messages.success(self.request, 'Lab order created successfully.')
        return super().form_valid(form)


class LabOrderDetailView(LoginRequiredMixin, DoctorLabOrPatientRequiredMixin, DetailView):
    model = LabOrder
    template_name = 'laboratory/lab_order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_patient:
            queryset = queryset.filter(patient__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('test')
        return context


class LabOrderUpdateView(LoginRequiredMixin, DoctorOrLabTechnicianRequiredMixin, UpdateView):
    model = LabOrder
    fields = ['status']
    template_name = 'laboratory/lab_order_form.html'
    success_url = reverse_lazy('laboratory:order_list')

    def form_valid(self, form):
        if form.cleaned_data['status'] == 'Completed':
            form.instance.completed_at = timezone.now()
        messages.success(self.request, 'Lab order status updated.')
        return super().form_valid(form)


class LabResultUploadView(LoginRequiredMixin, LabTechnicianRequiredMixin, CreateView):
    model = LabResult
    form_class = LabResultForm
    template_name = 'laboratory/lab_result_form.html'

    def form_valid(self, form):
        order_item = get_object_or_404(LabOrderItem, pk=self.kwargs['item_pk'])
        form.instance.order_item = order_item
        form.instance.uploaded_by = self.request.user

        order = order_item.order
        order.status = 'Completed'
        order.completed_at = timezone.now()
        order.save()

        messages.success(self.request, 'Lab result uploaded successfully.')
        return redirect('laboratory:order_detail', pk=order.pk)


class LabResultDetailView(LoginRequiredMixin, DoctorLabOrPatientRequiredMixin, DetailView):
    model = LabResult
    template_name = 'laboratory/lab_result_detail.html'
    context_object_name = 'result'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_patient:
            queryset = queryset.filter(order_item__order__patient__user=self.request.user)
        return queryset


class LabReportDownloadView(LoginRequiredMixin, DoctorLabOrPatientRequiredMixin, View):
    def get(self, request, pk):
        result = get_object_or_404(LabResult, pk=pk)
        if request.user.is_patient and result.order_item.order.patient.user != request.user:
            messages.error(request, 'You do not have permission to access this report.')
            return redirect('laboratory:order_list')
        if result.report_file:
            response = FileResponse(result.report_file.open('rb'), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{result.report_file.name}"'
            return response
        messages.error(request, 'No report file available for download.')
        return redirect('laboratory:order_list')


class LabReportPrintView(LoginRequiredMixin, DoctorLabOrPatientRequiredMixin, DetailView):
    model = LabOrder
    template_name = 'laboratory/lab_report_print.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_patient:
            queryset = queryset.filter(patient__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('test')
        return context


lab_test_list_view = LabTestListView.as_view()
lab_test_create_view = LabTestCreateView.as_view()
lab_test_update_view = LabTestUpdateView.as_view()
lab_order_list_view = LabOrderListView.as_view()
lab_order_create_view = LabOrderCreateView.as_view()
lab_order_detail_view = LabOrderDetailView.as_view()
lab_order_update_view = LabOrderUpdateView.as_view()
lab_result_upload_view = LabResultUploadView.as_view()
lab_result_detail_view = LabResultDetailView.as_view()
lab_report_download_view = LabReportDownloadView.as_view()
lab_report_print_view = LabReportPrintView.as_view()
