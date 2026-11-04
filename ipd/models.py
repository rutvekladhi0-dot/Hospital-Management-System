from django.db import models
from django.conf import settings


class Ward(models.Model):
    WARD_TYPE_CHOICES = [
        ('General', 'General'),
        ('Semi-Private', 'Semi-Private'),
        ('Private', 'Private'),
        ('ICU', 'ICU'),
        ('CCU', 'CCU'),
        ('ICCU', 'ICCU'),
    ]

    name = models.CharField(max_length=100)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='wards')
    floor = models.IntegerField(default=1)
    capacity = models.IntegerField(default=0)
    ward_type = models.CharField(max_length=15, choices=WARD_TYPE_CHOICES, default='General')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.ward_type})"

    @property
    def available_beds(self):
        return self.beds.filter(status='Available').count()

    @property
    def occupied_beds(self):
        return self.beds.filter(status='Occupied').count()

    @property
    def total_beds(self):
        return self.beds.count()

    @property
    def occupancy_percentage(self):
        total = self.total_beds
        if total == 0:
            return 0
        return round((self.occupied_beds / total) * 100, 1)

    @property
    def available_percentage(self):
        total = self.total_beds
        if total == 0:
            return 0
        return round((self.available_beds / total) * 100, 1)

    @property
    def rate_per_day(self):
        bed = self.beds.first()
        return bed.daily_rate if bed else 0


class Bed(models.Model):
    BED_TYPE_CHOICES = [
        ('Normal', 'Normal'),
        ('Oxygen', 'Oxygen'),
        ('Ventilator', 'Ventilator'),
        ('Cardiac', 'Cardiac'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Reserved', 'Reserved'),
        ('Maintenance', 'Maintenance'),
    ]

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    bed_type = models.CharField(max_length=15, choices=BED_TYPE_CHOICES, default='Normal')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Bed'
        verbose_name_plural = 'Beds'
        ordering = ['ward', 'bed_number']
        unique_together = ['ward', 'bed_number']

    def __str__(self):
        return f"Bed {self.bed_number} - {self.ward.name}"

    @property
    def current_patient(self):
        if self.status == 'Occupied':
            admission = Admission.objects.filter(bed=self, status='Admitted').first()
            if admission:
                return admission.patient
        return None


class Admission(models.Model):
    ADMISSION_TYPE_CHOICES = [
        ('Emergency', 'Emergency'),
        ('Elective', 'Elective'),
        ('Referral', 'Referral'),
    ]
    STATUS_CHOICES = [
        ('Admitted', 'Admitted'),
        ('Transferred', 'Transferred'),
        ('Discharged', 'Discharged'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='admissions')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='admissions')
    admission_date = models.DateTimeField(auto_now_add=True)
    admission_type = models.CharField(max_length=15, choices=ADMISSION_TYPE_CHOICES, default='Emergency')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='admissions')
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='admissions')
    diagnosis = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Admitted')
    discharge_date = models.DateTimeField(null=True, blank=True)
    discharge_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Admission'
        verbose_name_plural = 'Admissions'
        ordering = ['-admission_date']

    def __str__(self):
        return f"{self.admission_number} - {self.patient} - {self.ward.name} Bed {self.bed.bed_number}"

    @property
    def admission_number(self):
        return f"ADM-{str(self.pk).zfill(6)}"

    @property
    def expected_discharge_date(self):
        return self.discharge_date

    @property
    def discharge(self):
        try:
            return self.discharge_records.first()
        except Exception:
            return None

    @property
    def transfers(self):
        return self.bed_transfers.all()

    def save(self, *args, **kwargs):
        if self.status == 'Admitted' and self.bed.status != 'Occupied':
            self.bed.status = 'Occupied'
            self.bed.save()
        super().save(*args, **kwargs)


class BedTransfer(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='bed_transfers')
    from_ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='transfers_from')
    from_bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='transfers_from_bed')
    to_ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='transfers_to')
    to_bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='transfers_to_bed')
    transfer_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)
    transferred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='bed_transfers')

    class Meta:
        verbose_name = 'Bed Transfer'
        verbose_name_plural = 'Bed Transfers'
        ordering = ['-transfer_date']

    def __str__(self):
        return f"Transfer: {self.admission.patient} from {self.from_bed} to {self.to_bed}"

    def save(self, *args, **kwargs):
        self.from_bed.status = 'Available'
        self.from_bed.save()
        self.to_bed.status = 'Occupied'
        self.to_bed.save()
        self.admission.ward = self.to_ward
        self.admission.bed = self.to_bed
        self.admission.save()
        super().save(*args, **kwargs)
