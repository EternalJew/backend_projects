from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from api.serializers import UserSerializer
from api.models import User  
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import OutstandingToken
from django.db import transaction  
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from django.db import transaction, IntegrityError
import logging

User = get_user_model()

# Налаштування логування
logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    return Response({
                        'user': serializer.data,
                        'refresh': str(refresh),
                        'access': str(access_token),
                    }, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                logger.error(f"IntegrityError: {str(e)}, Request data: {serializer.validated_data}")
                return Response({'error': 'Failed to create user due to data integrity issue.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}, Request data: {serializer.validated_data}")
                return Response({'error': 'Failed to create user due to unexpected issue.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST']) #work
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Аутентифікація користувача
    user = authenticate(username=username, password=password)

    if user is not None:
        # Генерація токенів
        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))

        return Response({
            'username': username,
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Неправильний логін або пароль.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh_token = request.data.get('refresh')

    # Якщо токен не передано, повертаємо помилку
    if not refresh_token:
        return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Створюємо об'єкт RefreshToken
        token = RefreshToken(refresh_token)

        # Додаємо токен до blacklist
        token.blacklist()

        return Response({'message': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)
    except TokenError:
        return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) #work
@permission_classes([IsAuthenticated]) 
def profile(request):
    user = request.user  # Отримуємо аутентифікованого користувача
    profile_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
            'location': user.location,
            'is_available': user.is_available,
            'is_verified': user.is_verified,
            'created_at': user.created_at,
        }
    return Response(profile_data, status=status.HTTP_200_OK)
    
@api_view(['GET']) #work
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@api_view(['GET']) #work
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Це захищений ресурс, доступний тільки для аутентифікованих користувачів.'})
    
@api_view(['POST'])
def update_location(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    location_data = request.data.get('location')
    if location_data and 'latitude' in location_data and 'longitude' in location_data:
        user.location = location_data
        user.save()
        return Response({'message': 'Location updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid location data'}, status=status.HTTP_400_BAD_REQUEST)