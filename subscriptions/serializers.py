
from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'customer',
            'service',
            'start_date',
            'end_date',
            'status',
        ]
        read_only_fields = ['id', 'start_date']

    def validate_service(self, service):
        if not service.is_active:
            raise serializers.ValidationError(
                "This service is inactive and cannot be subscribed to."
            )

        return service
