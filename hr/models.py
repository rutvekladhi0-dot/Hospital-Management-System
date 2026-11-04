from django.db import models
from django.conf import settings


class Designation(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='designations')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'
        ordering = ['name']

    def __str__(self):
        return self.name


class HRRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('Appointment', 'Appointment'),
        ('Promotion', 'Promotion'),
        ('Transfer', 'Transfer'),
        ('Increment', 'Increment'),
        ('Warning', 'Warning'),
        ('Resignation', 'Resignation'),
    ]

    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='hr_records')
    record_type = models.CharField(max_length=15, choices=RECORD_TYPE_CHOICES)
    effective_date = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='hr_records')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'HR Record'
        verbose_name_plural = 'HR Records'
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.employee} - {self.record_type} ({self.effective_date})"


class Training(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trainer = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    employees = models.ManyToManyField('employees.Employee', related_name='trainings', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Planned')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} ({self.status})"
