from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import AssistanceRequest
from api.serializers import AssistanceRequestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.utils.create_coords_for_nav import get_route_coordinates
from geopy.distance import geodesic


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_assistance_request(request):
    print(f"Current user: {request.user}")  # Лог користувача

    if request.method == 'POST':
        serializer = AssistanceRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Прив'язуємо запит до поточного користувача
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# коли користувач натискає на кнопку "допомогти"
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_assistance_request(request, pk):
    try:
        assistance_request = AssistanceRequest.objects.get(pk=pk)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    assistance_request.status = 'accepted'
    assistance_request.service_provider = request.user  # Присвоюємо авторизованого користувача як service_provider
    assistance_request.save()

    # Отримуємо координати місця події
    event_location = assistance_request.location

    # Отримуємо координати користувача, який відкликнувся на допомогу
    responder_location = request.user.location

    # Серіалізуємо дані заявки
    serializer = AssistanceRequestSerializer(assistance_request)

    # Повертаємо відповідь із серіалізованими даними та координатами
    return Response({
        'assistance_request': serializer.data,
        'event_location': event_location,
        'responder_location': responder_location
    }, status=status.HTTP_200_OK)
    

# коли користувач натискає кнопку "почати поїздку" до місця надання допомоги
@api_view(['POST'])
def change_assistance_status_to_driving(request, pk):
    try:
        assistance_request = AssistanceRequest.objects.get(pk=pk)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Отримуємо координати користувача з request.data
    destination_point_dict = request.data.get('event_location')
    # Отримуємо координати респондента з request.data
    origin_point_dict = request.data.get('responder_location')
    
    if not origin_point_dict or not destination_point_dict:
        return Response({'error': 'Coordinates are required.'}, status=status.HTTP_400_BAD_REQUEST)

    #Використовуємо функцію get_route_coordinates з скрипта utils.create_coords_for_nav для отримання списка координат для побудови маршруту
    route_coords = get_route_coordinates(origin_point_dict, destination_point_dict)
    # Змінюємо статус на "is_driving"
    assistance_request.status = 'is_driving'
    assistance_request.save()

    # Серіалізуємо дані та повертаємо координати респондента і місця події
    serializer = AssistanceRequestSerializer(assistance_request)
    return Response({
        'assistance_request': serializer.data,
        'route_coordinates': route_coords,
    }, status=status.HTTP_200_OK)


# Коли водій приїде до місця поломки
@api_view(['POST'])
def change_assistance_status_to_resolving(request, pk):
    try:
        assistance_request = AssistanceRequest.objects.get(pk=pk)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)
    
     # Отримуємо координати користувача з request.data
    destination_point_dict = request.data.get('event_location')
    # Отримуємо координати респондента з request.data
    origin_point_dict = request.data.get('responder_location')
    
    if not destination_point_dict or not origin_point_dict:
        return Response({'error': 'Coordinates are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Перетворення координат з dict у кортежі
    destination_point = (destination_point_dict['latitude'], destination_point_dict['longitude'])
    origin_point = (origin_point_dict['latitude'], origin_point_dict['longitude'])

    # Обчислюємо відстань між респондентом та місцем події
    distance = geodesic(origin_point, destination_point).meters

    # Перевірка на радіус 30 метрів
    if distance <= 30:
        assistance_request.status = 'is_resolving'
        assistance_request.save()

        serializer = AssistanceRequestSerializer(assistance_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Responder is not within 50 meters of the event location.'}, status=status.HTTP_400_BAD_REQUEST)

# Коли користувач натисне кнопку "допомога була надана" 
#TODO Придумати спосіб закриття заявки у разі успішного її виконання
@api_view(['POST'])
def change_assistance_status_to_resolved(request, pk):
    try:
        assistance_request = AssistanceRequest.objects.get(pk=pk)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    assistance_request.status = 'resolved'
    assistance_request.save()

    serializer = AssistanceRequestSerializer(assistance_request)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def cancel_assistance_request(request, pk):
    try:
        assistance_request = AssistanceRequest.objects.get(pk=pk)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    assistance_request.status = 'cancelled'
    assistance_request.save()

    serializer = AssistanceRequestSerializer(assistance_request)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_assistance_by_id(request, pk):
    try:
        assistance = AssistanceRequest.objects.get(id=pk)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AssistanceRequestSerializer(assistance)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_assistance_by_id(request, assistance_id):
    try:
        assistance = AssistanceRequest.objects.get(id=assistance_id)
    except AssistanceRequest.DoesNotExist:
        return Response({'error': 'Assistance request not found'}, status=status.HTTP_404_NOT_FOUND)

    assistance.delete()

    return Response({'message': 'Assistance request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
