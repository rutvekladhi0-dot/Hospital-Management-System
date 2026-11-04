from django.db import models
from django.conf import settings
from hospitals.models import Branch


class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='departments')
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.branch})"


class Specialization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='specializations')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'
        ordering = ['name']

    def __str__(self):
        return self.name
