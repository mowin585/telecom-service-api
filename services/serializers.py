
from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'service_type',
            'description',
            'price',
            'validity_days',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
