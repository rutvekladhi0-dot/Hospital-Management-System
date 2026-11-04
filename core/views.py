from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import timedelta


@login_required
def home_view(request):
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    user = request.user
    context = {'today': timezone.now().date()}

    if user.is_superuser or _has_role(user, 'Super Admin') or _has_role(user, 'Hospital Admin'):
        return _admin_dashboard(request, context)
    elif _has_role(user, 'Doctor'):
        return _doctor_dashboard(request, context)
    elif _has_role(user, 'Patient'):
        return _patient_dashboard(request, context)
    elif _has_role(user, 'Nurse'):
        return _nurse_dashboard(request, context)
    elif _has_role(user, 'Receptionist'):
        return _receptionist_dashboard(request, context)
    elif _has_role(user, 'Pharmacist'):
        return _pharmacist_dashboard(request, context)
    elif _has_role(user, 'Lab Technician'):
        return _lab_dashboard(request, context)
    elif _has_role(user, 'Accountant'):
        return _accountant_dashboard(request, context)
    elif _has_role(user, 'HR Manager'):
        return _hr_dashboard(request, context)

    return render(request, 'core/dashboard.html', context)


def _has_role(user, role_name):
    try:
        return user.roles.filter(name=role_name).exists()
    except Exception:
        return False


def _admin_dashboard(request, context):
    context['role'] = 'admin'
    today = context['today']
    month_ago = today - timedelta(days=30)

    try:
        from accounts.models import User
        context['total_users'] = User.objects.count()
        context['total_doctors'] = User.objects.filter(roles__name='Doctor').distinct().count()
        context['total_patients'] = User.objects.filter(roles__name='Patient').distinct().count()
    except Exception:
        context['total_users'] = 0
        context['total_doctors'] = 0
        context['total_patients'] = 0

    try:
        from appointments.models import Appointment
        context['today_appointments'] = Appointment.objects.filter(appointment_date=today).count()
        context['total_appointments'] = Appointment.objects.count()
    except Exception:
        context['today_appointments'] = 0
        context['total_appointments'] = 0

    try:
        from billing.models import Invoice
        context['month_revenue'] = Invoice.objects.filter(
            created_at__date__gte=month_ago
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        context['pending_payments'] = Invoice.objects.filter(
            status='Pending'
        ).aggregate(total=Sum('due_amount'))['total'] or 0
    except Exception:
        context['month_revenue'] = 0
        context['pending_payments'] = 0

    try:
        from pharmacy.models import Medicine
        context['total_medicines'] = Medicine.objects.count()
        context['low_stock_count'] = Medicine.objects.filter(
            stock_quantity__lte=F('reorder_level')
        ).count()
    except Exception:
        context['total_medicines'] = 0
        context['low_stock_count'] = 0

    try:
        from laboratory.models import LabOrder
        context['pending_lab_orders'] = LabOrder.objects.filter(status='Pending').count()
    except Exception:
        context['pending_lab_orders'] = 0

    try:
        from patients.models import Patient
        context['total_patients'] = Patient.objects.count()
    except Exception:
        context['total_patients'] = 0

    try:
        from employees.models import Employee
        context['total_employees'] = Employee.objects.count()
    except Exception:
        context['total_employees'] = 0

    try:
        from ipd.models import Admission
        context['current_admissions'] = Admission.objects.filter(status='Admitted').count()
    except Exception:
        context['current_admissions'] = 0

    try:
        from notifications.models import Notification
        context['unread_notifications'] = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
    except Exception:
        context['unread_notifications'] = 0

    return render(request, 'core/dashboard.html', context)


def _doctor_dashboard(request, context):
    context['role'] = 'doctor'
    today = context['today']

    try:
        from doctors.models import Doctor
        context['doctor_profile'] = Doctor.objects.get(user=request.user)
    except Exception:
        context['doctor_profile'] = None

    try:
        from appointments.models import Appointment
        context['today_appointments'] = Appointment.objects.filter(
            doctor__user=request.user, appointment_date=today
        ).count()
        context['pending_appointments'] = Appointment.objects.filter(
            doctor__user=request.user, status='Scheduled'
        ).count()
        context['total_patients'] = Appointment.objects.filter(
            doctor__user=request.user
        ).values('patient').distinct().count()
    except Exception:
        context['today_appointments'] = 0
        context['pending_appointments'] = 0
        context['total_patients'] = 0

    return render(request, 'core/dashboard.html', context)


def _patient_dashboard(request, context):
    context['role'] = 'patient'
    today = context['today']

    try:
        from patients.models import Patient
        context['patient_profile'] = Patient.objects.get(user=request.user)
    except Exception:
        context['patient_profile'] = None

    try:
        from appointments.models import Appointment
        context['upcoming_appointments'] = Appointment.objects.filter(
            patient__user=request.user, appointment_date__gte=today
        ).order_by('appointment_date')[:5]
        context['total_appointments'] = Appointment.objects.filter(
            patient__user=request.user
        ).count()
    except Exception:
        context['upcoming_appointments'] = []
        context['total_appointments'] = 0

    try:
        from billing.models import Invoice
        context['pending_bills'] = Invoice.objects.filter(
            patient__user=request.user, status='Pending'
        ).count()
        context['total_paid'] = Invoice.objects.filter(
            patient__user=request.user, status='Paid'
        ).aggregate(total=Sum('paid_amount'))['total'] or 0
    except Exception:
        context['pending_bills'] = 0
        context['total_paid'] = 0

    try:
        from pharmacy.models import Prescription
        context['prescriptions'] = Prescription.objects.filter(
            patient__user=request.user
        ).order_by('-created_at')[:5]
    except Exception:
        context['prescriptions'] = []

    return render(request, 'core/dashboard.html', context)


def _nurse_dashboard(request, context):
    context['role'] = 'nurse'
    today = context['today']

    try:
        from nursing.models import NursingTask
        context['pending_tasks'] = NursingTask.objects.filter(
            assigned_to=request.user, status='Pending'
        ).count()
    except Exception:
        context['pending_tasks'] = 0

    try:
        from ipd.models import Admission
        context['current_admissions'] = Admission.objects.filter(status='Admitted').count()
    except Exception:
        context['current_admissions'] = 0

    try:
        from nursing.models import NursingTask
        context['completed_tasks'] = NursingTask.objects.filter(status='Completed').count()
    except Exception:
        context['completed_tasks'] = 0

    return render(request, 'core/dashboard.html', context)


def _receptionist_dashboard(request, context):
    context['role'] = 'receptionist'
    today = context['today']

    try:
        from appointments.models import Appointment
        context['today_appointments'] = Appointment.objects.filter(
            appointment_date=today
        ).count()
        context['pending_checkins'] = Appointment.objects.filter(
            appointment_date=today, status='Scheduled'
        ).count()
    except Exception:
        context['today_appointments'] = 0
        context['pending_checkins'] = 0

    try:
        from patients.models import Patient
        context['total_patients'] = Patient.objects.count()
    except Exception:
        context['total_patients'] = 0

    try:
        from ipd.models import Admission
        context['total_admissions'] = Admission.objects.count()
    except Exception:
        context['total_admissions'] = 0

    return render(request, 'core/dashboard.html', context)


def _pharmacist_dashboard(request, context):
    context['role'] = 'pharmacist'
    today = context['today']

    try:
        from pharmacy.models import Medicine
        context['total_medicines'] = Medicine.objects.count()
        context['low_stock'] = Medicine.objects.filter(
            stock_quantity__lte=F('reorder_level')
        ).count()
    except Exception:
        context['total_medicines'] = 0
        context['low_stock'] = 0

    try:
        from pharmacy.models import Prescription
        context['pending_prescriptions'] = Prescription.objects.filter(
            is_dispensed=False
        ).count()
    except Exception:
        context['pending_prescriptions'] = 0

    try:
        from pharmacy.models import DispensedMedicine
        context['dispensed_today'] = DispensedMedicine.objects.filter(
            dispensed_date__date=today
        ).count()
    except Exception:
        context['dispensed_today'] = 0

    return render(request, 'core/dashboard.html', context)


def _lab_dashboard(request, context):
    context['role'] = 'lab_technician'
    today = context['today']

    try:
        from laboratory.models import LabOrder
        context['pending_tests'] = LabOrder.objects.filter(status='Pending').count()
        context['completed_today'] = LabOrder.objects.filter(
            status='Completed', completed_at__date=today
        ).count()
    except Exception:
        context['pending_tests'] = 0
        context['completed_today'] = 0

    try:
        from laboratory.models import LabOrder
        context['total_lab_orders'] = LabOrder.objects.count()
    except Exception:
        context['total_lab_orders'] = 0

    return render(request, 'core/dashboard.html', context)


def _accountant_dashboard(request, context):
    context['role'] = 'accountant'
    today = context['today']
    month_ago = today - timedelta(days=30)

    try:
        from billing.models import Invoice
        context['month_revenue'] = Invoice.objects.filter(
            status='Paid', created_at__date__gte=month_ago
        ).aggregate(total=Sum('net_amount'))['total'] or 0
        context['pending_invoices'] = Invoice.objects.filter(
            status='Pending'
        ).count()
        context['total_pending_amount'] = Invoice.objects.filter(
            status='Pending'
        ).aggregate(total=Sum('due_amount'))['total'] or 0
    except Exception:
        context['month_revenue'] = 0
        context['pending_invoices'] = 0
        context['total_pending_amount'] = 0

    try:
        from billing.models import Invoice
        context['total_invoices'] = Invoice.objects.count()
    except Exception:
        context['total_invoices'] = 0

    return render(request, 'core/dashboard.html', context)


def _hr_dashboard(request, context):
    context['role'] = 'hr_manager'
    today = context['today']

    try:
        from employees.models import Employee
        context['total_employees'] = Employee.objects.count()
    except Exception:
        context['total_employees'] = 0

    try:
        from employees.models import LeaveRequest
        context['pending_leaves'] = LeaveRequest.objects.filter(
            status='Pending'
        ).count()
    except Exception:
        context['pending_leaves'] = 0

    try:
        from departments.models import Department
        context['total_departments'] = Department.objects.count()
    except Exception:
        context['total_departments'] = 0

    return render(request, 'core/dashboard.html', context)
