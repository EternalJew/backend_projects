from django.contrib import admin
from django.urls import path
from api.views.admin_panel_views import (TodoGetCreate, TodoUpdateDelete, UserGetCreate, UserUpdateDelete,
                    AssistanceRequestGetCreate, AssistanceRequestUpdateDelete, ServiceProviderGetCreate,
                    ServiceProviderUpdateDelete, NotificationGetCreate, NotificationUpdateDelete,
                    RatingGetCreate, RatingUpdateDelete, PaymentGetCreate, PaymentUpdateDelete, AssistanceRequests)
from api.views.user_view import create_user, get_users, get_user_by_id, login_user, logout_user, profile
from api.views.assistance_request_view import (get_assistance_by_id, delete_assistance_by_id, create_assistance_request, 
                                                accept_assistance_request, change_assistance_status_to_driving, 
                                                change_assistance_status_to_resolving, change_assistance_status_to_resolved,
                                                cancel_assistance_request
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.rating_view import create_rating, get_service_provider_ratings, get_user_given_ratings, top_users

urlpatterns = [
    #Todo
    path('todo/', TodoGetCreate.as_view()),
    path('todo/<int:pk>', TodoUpdateDelete.as_view()),
    #User
    path('user/', UserGetCreate.as_view()),
    path('user/<int:pk>', UserUpdateDelete.as_view()),
    #AssistanceRequest
    path('assistance/', AssistanceRequestGetCreate.as_view()),
    path('assistance/<int:pk>', AssistanceRequestUpdateDelete.as_view()),
    #ServiceProvider
    path('service_provider/', ServiceProviderGetCreate.as_view()),
    path('service_provider/<int:pk>', ServiceProviderUpdateDelete.as_view()),
    #Notification
    path('notification/', NotificationGetCreate.as_view()),
    path('notification/<int:pk>', NotificationUpdateDelete.as_view()),
    #Rating
    path('rating/', RatingGetCreate.as_view()),
    path('rating/<int:pk>', RatingUpdateDelete.as_view()),
    #Paymant
    path('paymant/', PaymentGetCreate.as_view()),
    path('paymant/<int:pk>', PaymentUpdateDelete.as_view()),

    #API
    #USER
    path('user/create/', create_user, name='create_user'),
    path('user/login/', login_user, name='login'),
    path('user/logout/', logout_user, name='logout'),
    path('user/profile/', profile, name='profile'),
    path('user/get_all/', get_users, name='get_all_users'),
    path('user/get_by_id/<int:user_id>', get_user_by_id, name='get_user_by_id'),
    path('user/token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #приймає собі username і password і видає токен
    path('user/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    #AssistanceRequest
    path('assistance_request/create/', create_assistance_request, name='assistance_request_create'),
    path('assistance_request/<int:pk>/accept', accept_assistance_request, name='request_accepting'),
    path('assistance_request/<int:pk>/driving', change_assistance_status_to_driving, name='driveng'),
    path('assistance_request/<int:pk>/resolving', change_assistance_status_to_resolving, name='resolving'),
    path('assistance_request/<int:pk>/resolved', change_assistance_status_to_resolved, name='resolved'),
    path('assistance_request/<int:pk>/cancel', cancel_assistance_request, name='cancel'),
    path('assistance_request/get_by_id/<int:pk>/', get_assistance_by_id, name='get_assistance_by_id'),
    path('assistance_request/delete/<int:pk>', delete_assistance_by_id, name='delete_assistance_by_id'),

    #Rating
    path('rating/<int:pk>/create', create_rating, name='create_rating'),
    path('rating/<int:pk>/service_provider_ratings', get_service_provider_ratings, name='service_provider_ratings'),
    path('rating/current_user_given_ratings', get_user_given_ratings, name='current_user_given_ratings'),
    path('rating/top_users', top_users, name='top_users'),
]