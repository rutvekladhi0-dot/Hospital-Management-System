from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import AuditLog
from .forms import AuditLogFilterForm


@staff_member_required
def audit_log_list_view(request):
    form = AuditLogFilterForm(request.GET or None)
    queryset = AuditLog.objects.select_related('user').all()

    if form.is_valid():
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        user = form.cleaned_data.get('user')
        action = form.cleaned_data.get('action')

        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        if user:
            queryset = queryset.filter(user=user)
        if action:
            queryset = queryset.filter(action=action)

    context = {
        'form': form,
        'logs': queryset[:500],
        'table_id': 'auditLogTable',
    }
    return render(request, 'auditlogs/auditlog_list.html', context)


@staff_member_required
def audit_log_detail_view(request, pk):
    log = get_object_or_404(AuditLog.objects.select_related('user'), pk=pk)
    context = {
        'log': log,
    }
    return render(request, 'auditlogs/auditlog_detail.html', context)
