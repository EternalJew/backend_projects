from django.contrib import admin
from .models import Todo, User, AssistanceRequest, ServiceProvider, Notification, Rating, Payment

# Register your models here.
admin.site.register(Todo)
admin.site.register(User)
admin.site.register(AssistanceRequest)
admin.site.register(ServiceProvider)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(Payment)