
from django.db import models


class Service(models.Model):
    SERVICE_TYPES = [
        ('DATA', 'Data Bundle'),
        ('VOICE', 'Voice Package'),
        ('SMS', 'SMS Package'),
    ]

    name = models.CharField(max_length=100)
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPES
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
