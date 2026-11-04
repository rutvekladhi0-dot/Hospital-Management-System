from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import OPDVisit
from .forms import OPDVisitForm
from core.mixins import DoctorRequiredMixin


class OPDListView(LoginRequiredMixin, DoctorRequiredMixin, ListView):
    model = OPDVisit
    template_name = 'opd/opd_list.html'
    context_object_name = 'opd_visits'
    paginate_by = 25

    def get_queryset(self):
        queryset = OPDVisit.objects.select_related('patient', 'doctor', 'doctor__employee', 'doctor__employee__user')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        date = self.request.GET.get('date')

        if search:
            queryset = queryset.filter(
                Q(opd_number__icontains=search) |
                Q(patient__patient_id__icontains=search) |
                Q(patient__user__first_name__icontains=search) |
                Q(patient__user__last_name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        if date:
            queryset = queryset.filter(visit_date=date)
        else:
            queryset = queryset.filter(visit_date=timezone.now().date())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = 'opdTable'
        context['today'] = timezone.now().date()
        context['total_today'] = OPDVisit.objects.filter(visit_date=timezone.now().date()).count()
        context['waiting'] = OPDVisit.objects.filter(visit_date=timezone.now().date(), status='Waiting').count()
        context['in_progress'] = OPDVisit.objects.filter(visit_date=timezone.now().date(), status='In-Progress').count()
        context['completed'] = OPDVisit.objects.filter(visit_date=timezone.now().date(), status='Completed').count()
        return context


opd_list_view = OPDListView.as_view()


class OPDCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = OPDVisit
    form_class = OPDVisitForm
    template_name = 'opd/opd_form.html'
    success_url = reverse_lazy('opd:opd_list')

    def form_valid(self, form):
        if not form.instance.visit_date:
            form.instance.visit_date = timezone.now().date()
        messages.success(self.request, 'OPD visit created successfully.')
        return super().form_valid(form)


opd_create_view = OPDCreateView.as_view()


class OPDDetailView(LoginRequiredMixin, DoctorRequiredMixin, DetailView):
    model = OPDVisit
    template_name = 'opd/opd_detail.html'
    context_object_name = 'opd_visit'


opd_detail_view = OPDDetailView.as_view()


class OPDUpdateView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = OPDVisit
    form_class = OPDVisitForm
    template_name = 'opd/opd_form.html'
    success_url = reverse_lazy('opd:opd_list')

    def form_valid(self, form):
        messages.success(self.request, 'OPD visit updated successfully.')
        return super().form_valid(form)


opd_update_view = OPDUpdateView.as_view()


class OPDCompleteView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = OPDVisit
    template_name = 'opd/opd_form.html'
    fields = ['diagnosis', 'treatment', 'doctor_notes', 'follow_up_date', 'status']
    success_url = reverse_lazy('opd:opd_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opd_visit'] = self.object
        return context

    def form_valid(self, form):
        form.instance.status = 'Completed'
        messages.success(self.request, 'OPD visit completed successfully.')
        return super().form_valid(form)


opd_complete_view = OPDCompleteView.as_view()
