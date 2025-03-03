from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import ServiceProvider
from api.serializers import ServiceProviderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service(request):
    if request.method == 'POST':
        serializer = ServiceProviderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_service_by_id(request, user_id):
    try:
        service = ServiceProvider.objects.get(id=user_id)
    except ServiceProvider.DoesNotExist:
        return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceProviderSerializer(service)
    return Response(serializer.data)


@api_view(['GET'])
def get_service_all(request):
    try:
        service = ServiceProvider.objects.all()
    except ServiceProvider.DoesNotExist:
        return Response({'error': 'Services not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceProviderSerializer(service, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_service_by_id(request, service_id):
    try:
        service = ServiceProvider.objects.get(id=service_id)
    except ServiceProvider.DoesNotExist:
        return Response({'error': 'Service provider not found'}, status=status.HTTP_404_NOT_FOUND)

    service.delete()

    return Response({'message': 'Service provider deleted successfully'}, status=status.HTTP_204_NO_CONTENT)