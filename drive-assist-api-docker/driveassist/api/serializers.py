from rest_framework import serializers
from .models import Todo, User, AssistanceRequest, ServiceProvider, Notification, Rating, Payment
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'location', 'is_available', 'is_verified', 'password', 'avg_rating']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': [UniqueValidator(queryset=User.objects.all())]},
            'email': {'validators': [UniqueValidator(queryset=User.objects.all())]},
            }

    def create(self, validated_data):
        try:
            user = User(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")

class AssistanceRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    class Meta:
        model = AssistanceRequest
        fields = ['id', 'user', 'username', 'phone_number','description_title', 'accident_category', 'description', 'location', 'location_desc', 'status', 'backup_user_number', 'created_at', 'resolved_at', 'service_provider']
        read_only_fields = ['id', 'user', 'created_at', 'resolved_at', 'status']

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'