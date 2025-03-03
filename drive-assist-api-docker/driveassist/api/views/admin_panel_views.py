from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Todo, User, AssistanceRequest, ServiceProvider, Notification, Rating, Payment
from api.serializers import (TodoSerializer, UserSerializer, AssistanceRequestSerializer,
                          ServiceProviderSerializer, NotificationSerializer, RatingSerializer, PaymentSerializer)


#API VIEWS
class AssistanceRequests(APIView):
    def post(self, request):
        serializer = AssistanceRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Зберігаємо новий запит на допомогу
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ADMIN VIEWS
class TodoGetCreate(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class UserGetCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AssistanceRequestGetCreate(generics.ListCreateAPIView):
    queryset = AssistanceRequest.objects.all()
    serializer_class = AssistanceRequestSerializer

class AssistanceRequestUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ServiceProviderGetCreate(generics.ListCreateAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class ServiceProviderUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class NotificationGetCreate(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class RatingGetCreate(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class PaymentGetCreate(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer