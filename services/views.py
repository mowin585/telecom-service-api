
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Service
from .serializers import ServiceSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def service_list(request):
    if request.method == 'GET':
        services = Service.objects.all().order_by('id')
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    serializer = ServiceSerializer(data=request.data)
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
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ServiceSerializer(
            service,
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

    service.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
