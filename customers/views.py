from rest_framework import filters
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def customer_list(request):
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('-created_at')

        search = request.query_params.get('search')

        if search:
            from django.db.models import Q

            customers = customers.filter(
                Q(full_name__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(email__icontains=search)
            )

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = CustomerSerializer(
            customer,
            data=request.data,
            partial=partial
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
