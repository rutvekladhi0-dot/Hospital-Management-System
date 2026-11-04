from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from .models import Invoice, InvoiceItem, Payment, PaymentReceipt
from .forms import InvoiceForm, InvoiceItemForm, PaymentForm, InvoiceFilterForm
from core.mixins import AccountantRequiredMixin, PatientOrAccountantRequiredMixin, BillingViewMixin


class InvoiceListView(LoginRequiredMixin, BillingViewMixin, ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 25

    def get_queryset(self):
        queryset = Invoice.objects.select_related('patient', 'created_by')
        if self.request.user.is_patient:
            queryset = queryset.filter(patient__user=self.request.user)
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search) |
                Q(patient__patient_id__icontains=search) |
                Q(patient__user__first_name__icontains=search) |
                Q(patient__user__last_name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'invoiceTable'
        context['filter_form'] = InvoiceFilterForm(self.request.GET)
        context['total_invoices'] = Invoice.objects.count()
        context['total_pending'] = Invoice.objects.filter(status='Pending').count()
        context['total_paid'] = Invoice.objects.filter(status='Paid').count()
        context['total_revenue'] = Invoice.objects.filter(status='Paid').aggregate(total=Sum('net_amount'))['total'] or 0
        return context


invoice_list_view = InvoiceListView.as_view()


class InvoiceCreateView(LoginRequiredMixin, AccountantRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('billing:invoice_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Invoice created successfully.')
        return super().form_valid(form)


invoice_create_view = InvoiceCreateView.as_view()


class InvoiceUpdateView(LoginRequiredMixin, AccountantRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('billing:invoice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Invoice updated successfully.')
        return super().form_valid(form)


invoice_update_view = InvoiceUpdateView.as_view()


class InvoiceDetailView(LoginRequiredMixin, PatientOrAccountantRequiredMixin, DetailView):
    model = Invoice
    template_name = 'billing/invoice_detail.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_patient:
            queryset = queryset.filter(patient__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        context['payments'] = self.object.payments.all()
        context['item_form'] = InvoiceItemForm()
        context['payment_form'] = PaymentForm()
        return context


invoice_detail_view = InvoiceDetailView.as_view()


class InvoiceDeleteView(LoginRequiredMixin, AccountantRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('billing:invoice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Invoice deleted successfully.')
        return super().form_valid(form)


invoice_delete_view = InvoiceDeleteView.as_view()


class InvoicePrintView(LoginRequiredMixin, PatientOrAccountantRequiredMixin, DetailView):
    model = Invoice
    template_name = 'billing/invoice_print.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_patient:
            queryset = queryset.filter(patient__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        context['payments'] = self.object.payments.all()
        return context


invoice_print_view = InvoicePrintView.as_view()


@login_required
def payment_create_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.received_by = request.user
            payment.save()
            PaymentReceipt.objects.create(payment=payment)
            if invoice.is_fully_paid:
                invoice.status = 'Paid'
                invoice.save()
            elif invoice.paid_amount > 0:
                invoice.status = 'Partial'
                invoice.save()
            messages.success(request, 'Payment recorded successfully.')
            return redirect('billing:invoice_detail', pk=invoice.pk)
    else:
        form = PaymentForm()
    return render(request, 'billing/payment_form.html', {'form': form, 'invoice': invoice})


class PaymentListView(LoginRequiredMixin, AccountantRequiredMixin, ListView):
    model = Payment
    template_name = 'billing/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_queryset(self):
        return Payment.objects.select_related('invoice', 'received_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'paymentTable'
        return context


payment_list_view = PaymentListView.as_view()


class PaymentDetailView(LoginRequiredMixin, AccountantRequiredMixin, DetailView):
    model = Payment
    template_name = 'billing/payment_detail.html'
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['receipt'] = self.object.receipt
        except PaymentReceipt.DoesNotExist:
            context['receipt'] = None
        return context


payment_detail_view = PaymentDetailView.as_view()


class DueListView(LoginRequiredMixin, AccountantRequiredMixin, ListView):
    model = Invoice
    template_name = 'billing/due_list.html'
    context_object_name = 'invoices'
    paginate_by = 25

    def get_queryset(self):
        return Invoice.objects.filter(due_amount__gt=0).select_related('patient')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'dueTable'
        context['total_due'] = Invoice.objects.filter(due_amount__gt=0).aggregate(
            total=Sum('due_amount')
        )['total'] or 0
        return context


due_list_view = DueListView.as_view()


class RevenueReportView(LoginRequiredMixin, AccountantRequiredMixin, ListView):
    model = Invoice
    template_name = 'billing/revenue_report.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.filter(status='Paid')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        context['total_revenue'] = Invoice.objects.filter(status='Paid').aggregate(
            total=Sum('net_amount'))['total'] or 0
        context['today_revenue'] = Invoice.objects.filter(
            status='Paid', created_at__date=today).aggregate(
            total=Sum('net_amount'))['total'] or 0
        context['weekly_revenue'] = Invoice.objects.filter(
            status='Paid', created_at__date__gte=week_ago).aggregate(
            total=Sum('net_amount'))['total'] or 0
        context['monthly_revenue'] = Invoice.objects.filter(
            status='Paid', created_at__date__gte=month_ago).aggregate(
            total=Sum('net_amount'))['total'] or 0
        context['total_outstanding'] = Invoice.objects.filter(
            due_amount__gt=0).aggregate(total=Sum('due_amount'))['total'] or 0
        return context


revenue_report_view = RevenueReportView.as_view()


@login_required
def add_invoice_item_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.save()
            invoice.total_amount = invoice.items.aggregate(
                total=Sum('total_price'))['total'] or 0
            invoice.save()
            messages.success(request, 'Item added to invoice.')
            return redirect('billing:invoice_detail', pk=invoice.pk)
    return redirect('billing:invoice_detail', pk=invoice.pk)


@login_required
def delete_invoice_item_view(request, item_id):
    item = get_object_or_404(InvoiceItem, pk=item_id)
    invoice = item.invoice
    item.delete()
    invoice.total_amount = invoice.items.aggregate(
        total=Sum('total_price'))['total'] or 0
    invoice.save()
    messages.success(request, 'Item removed from invoice.')
    return redirect('billing:invoice_detail', pk=invoice.pk)
