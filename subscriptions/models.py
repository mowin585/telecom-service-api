
from django.db import models


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    service = models.ForeignKey(
        'services.Service',
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    def __str__(self):
        return f"{self.customer.full_name} - {self.service.name}"
