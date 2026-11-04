from django.db import models


class InsuranceProvider(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Insurance Provider'
        verbose_name_plural = 'Insurance Providers'
        ordering = ['name']

    def __str__(self):
        return self.name


class InsurancePlan(models.Model):
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=200)
    coverage_percentage = models.IntegerField(default=0)
    max_coverage = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Insurance Plan'
        verbose_name_plural = 'Insurance Plans'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.provider.name})"


class PatientInsurance(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='insurances')
    plan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE, related_name='patient_insurances')
    policy_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Patient Insurance'
        verbose_name_plural = 'Patient Insurances'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient} - {self.plan.name} ({self.policy_number})"

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.end_date < timezone.now().date()
