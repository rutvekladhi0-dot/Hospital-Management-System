from django.db import models
from django.conf import settings


class NursingStation(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey('ipd.Ward', on_delete=models.CASCADE, related_name='nursing_stations')
    capacity = models.IntegerField(default=10)
    nurse_in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='nursing_stations_in_charge')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nursing Station'
        verbose_name_plural = 'Nursing Stations'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.ward.name}"

    @property
    def head_nurse(self):
        return self.nurse_in_charge

    @property
    def floor(self):
        return self.ward.floor

    @property
    def wards(self):
        return [self.ward]

    @property
    def is_active(self):
        return True


class NursingTask(models.Model):
    TASK_TYPE_CHOICES = [
        ('Medication', 'Medication'),
        ('Vitals', 'Vitals'),
        ('Wound Care', 'Wound Care'),
        ('IV', 'IV'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
        ('Skipped', 'Skipped'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='nursing_tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nursing_tasks')
    task_type = models.CharField(max_length=15, choices=TASK_TYPE_CHOICES)
    description = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nursing Task'
        verbose_name_plural = 'Nursing Tasks'
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.get_task_type_display()} - {self.patient} ({self.status})"


class VitalSigns(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='vital_signs')
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='vital_signs_recorded')
    temperature = models.DecimalField(max_digits=5, decimal_places=1, help_text='Temperature in °F')
    blood_pressure_systolic = models.IntegerField(help_text='Systolic (mmHg)')
    blood_pressure_diastolic = models.IntegerField(help_text='Diastolic (mmHg)')
    heart_rate = models.IntegerField(help_text='Heart rate (bpm)')
    respiratory_rate = models.IntegerField(help_text='Respiratory rate (breaths/min)', null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text='SpO2 (%)')
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Weight in kg')
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vital Signs'
        verbose_name_plural = 'Vital Signs'
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Vitals: {self.patient} - {self.recorded_at}"

    @property
    def blood_pressure(self):
        return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
