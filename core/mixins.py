from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return True
        return self.request.user.roles.filter(name__in=self.allowed_roles).exists()

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(self.request.get_full_path(), self.get_login_url())


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Super Admin', 'Hospital Admin']


class DoctorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor']


class PatientRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Patient']


class NurseRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Nurse']


class ReceptionistRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Receptionist']


class PharmacistRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Pharmacist']


class LabTechnicianRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Lab Technician']


class DoctorOrLabTechnicianRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor', 'Lab Technician']


class DoctorOrPharmacistRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor', 'Pharmacist']


class DoctorLabOrPatientRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor', 'Lab Technician', 'Patient']


class DoctorPharmacistOrPatientRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor', 'Pharmacist', 'Patient']


class PatientOrAccountantRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Patient', 'Accountant']


class BillingViewMixin(RoleRequiredMixin):
    allowed_roles = ['Patient', 'Accountant', 'Receptionist']


class NurseOrAdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Nurse', 'Super Admin', 'Hospital Admin']


class AppointmentViewMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor', 'Patient', 'Receptionist', 'Nurse', 'Super Admin', 'Hospital Admin']


class AccountantRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Accountant']


class HRManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['HR Manager']
