from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class User(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(Role, blank=True, related_name='users')

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.username

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    @property
    def is_super_admin(self):
        return self.is_superuser

    @property
    def is_hospital_admin(self):
        return self.has_role('Hospital Admin')

    @property
    def is_doctor(self):
        return self.has_role('Doctor')

    @property
    def is_nurse(self):
        return self.has_role('Nurse')

    @property
    def is_receptionist(self):
        return self.has_role('Receptionist')

    @property
    def is_pharmacist(self):
        return self.has_role('Pharmacist')

    @property
    def is_lab_technician(self):
        return self.has_role('Lab Technician')

    @property
    def is_accountant(self):
        return self.has_role('Accountant')

    @property
    def is_hr_manager(self):
        return self.has_role('HR Manager')

    @property
    def is_patient(self):
        return self.has_role('Patient')
