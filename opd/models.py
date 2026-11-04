from django.db import models
from django.conf import settings


class OPDVisit(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
        ('Referred', 'Referred'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='opd_visits')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='opd_visits')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='opd_visits')
    opd_number = models.CharField(max_length=20, unique=True, editable=False)
    visit_date = models.DateField()
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    doctor_notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'OPD Visit'
        verbose_name_plural = 'OPD Visits'
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        return f"{self.opd_number} - {self.patient} with {self.doctor}"

    def save(self, *args, **kwargs):
        if not self.opd_number:
            last = OPDVisit.objects.all().order_by('-id').first()
            if last:
                last_num = int(last.opd_number.split('-')[1])
                self.opd_number = f'OPD-{str(last_num + 1).zfill(6)}'
            else:
                self.opd_number = 'OPD-000001'
        super().save(*args, **kwargs)

    @property
    def department(self):
        try:
            return self.doctor.employee.department
        except Exception:
            return None

    @property
    def chief_complaint(self):
        return self.symptoms
