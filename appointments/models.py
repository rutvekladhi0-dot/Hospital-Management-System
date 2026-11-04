from django.db import models
from django.conf import settings


class Appointment(models.Model):
    APPOINTMENT_TYPE_CHOICES = [
        ('OPD', 'OPD'),
        ('IPD', 'IPD'),
        ('EMERGENCY', 'Emergency'),
        ('ONLINE', 'Online'),
    ]

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Confirmed', 'Confirmed'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-Show', 'No-Show'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    appointment_type = models.CharField(max_length=10, choices=APPOINTMENT_TYPE_CHOICES, default='OPD')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Scheduled')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date}"

    @property
    def patient_name(self):
        return self.patient.user.get_full_name()

    @property
    def doctor_name(self):
        return self.doctor.employee.user.get_full_name()


class Visit(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='visit')
    doctor_notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'
        ordering = ['-created_at']

    def __str__(self):
        return f"Visit for {self.appointment}"
