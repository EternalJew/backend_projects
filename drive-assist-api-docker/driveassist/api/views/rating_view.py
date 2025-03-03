from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Rating, User, AssistanceRequest
from api.serializers import RatingSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Avg


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rating(request, service_provider_id):
    user = request.user
    service_provider = get_object_or_404(User, id=service_provider_id)

    request_instance = AssistanceRequest.objects.filter(
        user=user, 
        service_provider=service_provider, 
        status__in=['resolved', 'cancelled']
    ).first()

    if not request_instance:
        return Response(
            {"error": "Rating can only be left after the request is resolved or cancelled."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, service_provider=service_provider)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Отримання всіх рейтингів, які отримав певний надавач допомоги
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_service_provider_ratings(request, service_provider_id):
    ratings = Rating.objects.filter(service_provider_id=service_provider_id)
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Отримання всіх рейтингів, які залишив авторизований користувач
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_given_ratings(request):
    ratings = Rating.objects.filter(user=request.user)
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def top_users(request):
    top_service_providers = (
        User.objects
        .filter(received_ratings__isnull=False)  # Користувачі, які мають рейтинги
        .annotate(avg_rating=Avg('received_ratings__rating_value'))  # Додавання середнього рейтингу
        .order_by('-avg_rating')[:10]  # Отримання топ-10 користувачів
    )

    serializer = UserSerializer(top_service_providers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)