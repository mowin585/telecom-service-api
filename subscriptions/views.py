
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer


def expire_subscription_if_needed(subscription):
    if (
        subscription.status == 'ACTIVE'
        and subscription.end_date <= timezone.now()
    ):
        subscription.status = 'EXPIRED'
        subscription.save(update_fields=['status'])

    return subscription


def expire_all_past_due_subscriptions():
    Subscription.objects.filter(
        status='ACTIVE',
        end_date__lte=timezone.now(),
    ).update(status='EXPIRED')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def subscription_list(request):
    if request.method == 'GET':
        expire_all_past_due_subscriptions()

        subscriptions = Subscription.objects.select_related(
            'customer', 'service'
        ).order_by('id')

        customer_id = request.query_params.get('customer')
        subscription_status = request.query_params.get('status')

        if customer_id:
            subscriptions = subscriptions.filter(
                customer_id=customer_id
            )

        if subscription_status:
            subscriptions = subscriptions.filter(
                status=subscription_status.upper()
            )

        serializer = SubscriptionSerializer(
            subscriptions,
            many=True,
        )
        return Response(serializer.data)

    serializer = SubscriptionSerializer(data=request.data)

    if serializer.is_valid():
        subscription = serializer.save()
        expire_subscription_if_needed(subscription)

        return Response(
            SubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def subscription_detail(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    expire_subscription_if_needed(subscription)

    if request.method == 'GET':
        return Response(SubscriptionSerializer(subscription).data)

    if request.method == 'PATCH':
        serializer = SubscriptionSerializer(
            subscription,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            subscription = serializer.save()
            expire_subscription_if_needed(subscription)

            return Response(
                SubscriptionSerializer(subscription).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    subscription.status = 'CANCELLED'
    subscription.save(update_fields=['status'])

    return Response(
        SubscriptionSerializer(subscription).data,
        status=status.HTTP_200_OK,
    )
