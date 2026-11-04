from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('Appointment', 'Appointment'),
        ('Billing', 'Billing'),
        ('Laboratory', 'Laboratory'),
        ('Pharmacy', 'Pharmacy'),
        ('General', 'General'),
        ('Alert', 'Alert'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='General')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.recipient.username}"

    @property
    def type_badge_class(self):
        badge_map = {
            'Appointment': 'bg-primary',
            'Billing': 'bg-success',
            'Laboratory': 'bg-info',
            'Pharmacy': 'bg-warning text-dark',
            'General': 'bg-secondary',
            'Alert': 'bg-danger',
        }
        return badge_map.get(self.notification_type, 'bg-secondary')

    @property
    def url(self):
        return self.link if self.link else None
