from django.db import models
from django.conf import settings


class Ambulance(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Basic', 'Basic'),
        ('AC', 'AC'),
        ('ICU', 'ICU'),
    ]

    vehicle_number = models.CharField(max_length=30, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='Basic')
    is_available = models.BooleanField(default=True)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=20)
    current_location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ambulance'
        verbose_name_plural = 'Ambulances'
        ordering = ['vehicle_number']

    def __str__(self):
        return f"{self.vehicle_number} ({self.vehicle_type})"


class AmbulanceRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Dispatched', 'Dispatched'),
        ('In-Transit', 'In-Transit'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20)
    pickup_location = models.CharField(max_length=300)
    dropoff_location = models.CharField(max_length=300)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ambulance_requests')
    dispatched_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ambulance Request'
        verbose_name_plural = 'Ambulance Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient_name} - {self.status}"
