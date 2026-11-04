from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def _role_required(allowed_roles, redirect_url='home'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or request.user.roles.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access this page.')
            return redirect(redirect_url)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    return _role_required(['Super Admin', 'Hospital Admin'])(view_func)


def doctor_required(view_func):
    return _role_required(['Doctor'])(view_func)


def patient_required(view_func):
    return _role_required(['Patient'])(view_func)


def receptionist_required(view_func):
    return _role_required(['Receptionist'])(view_func)


def pharmacist_required(view_func):
    return _role_required(['Pharmacist'])(view_func)


def lab_required(view_func):
    return _role_required(['Lab Technician'])(view_func)
