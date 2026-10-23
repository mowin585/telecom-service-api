
from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
