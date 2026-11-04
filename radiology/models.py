from django.db import models
from django.conf import settings


class RadiologyTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Radiology Tests'

    def __str__(self):
        return self.name


class RadiologyOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In-Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('Routine', 'Routine'),
        ('Urgent', 'Urgent'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='radiology_orders')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='radiology_orders')
    test = models.ForeignKey(RadiologyTest, on_delete=models.CASCADE, related_name='orders')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    clinical_information = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Routine')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Radiology Order #{self.order_number} - {self.test.name}"

    @property
    def order_number(self):
        return f"RAD-{str(self.pk).zfill(6)}"


class RadiologyReport(models.Model):
    order = models.OneToOneField(RadiologyOrder, on_delete=models.CASCADE, related_name='report')
    findings = models.TextField()
    impression = models.TextField()
    image_file = models.FileField(upload_to='radiology/images/', blank=True)
    report_file = models.FileField(upload_to='radiology/reports/', blank=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Radiology Reports'

    def __str__(self):
        return f"Report for Order #{self.order.order_number}"

    @property
    def created_by(self):
        return self.reported_by

    @property
    def notes(self):
        return self.findings

    @property
    def images(self):
        return RadiologyImage.objects.filter(report=self)


class RadiologyImage(models.Model):
    report = models.ForeignKey(RadiologyReport, on_delete=models.CASCADE, related_name='image_set')
    image = models.FileField(upload_to='radiology/images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for {self.report}"
