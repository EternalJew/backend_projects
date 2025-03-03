from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('workshop', 'Workshop'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='driver')
    location = models.JSONField(null=True, blank=True)  # {'latitude': ..., 'longitude': ...}
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class AssistanceRequest(models.Model): #запит на допомогу
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('accepted', 'Accepted'),
        ('is_driving', 'Is driving'),
        ('is_resolving', 'Is resolving'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]

    ACCIDENT_CATEGORY = [
        ('none', 'None'),
        ('chassis', 'Chassis'),
        ('engine', 'Engine'),
        ('accident','Accident'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistance_requests', null=False, blank=True)
    description_title = models.CharField(max_length=150, unique=False, null=True)
    accident_category = models.CharField(max_length=20, choices=ACCIDENT_CATEGORY, default='none')
    description = models.CharField(max_length=150, unique=False)
    location = models.JSONField(null=True, blank=True)   # {'latitude': ..., 'longitude': ...}
    location_desc = models.CharField(max_length=150, unique=False, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    backup_user_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    service_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_requests')

    def __str__(self):
        return f"Request {self.id} by {self.user.username}"

class ServiceProvider(models.Model): #майстерні або технічна допомога
    SERVICE_CHOICES = [
        ('wheel_replacement', 'Wheel Replacement'),
        ('towing', 'Towing'),
        # Add more types of services as needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='service_provider')
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    availability_radius = models.IntegerField(default=10)  # in kilometers
    location = models.JSONField()  # {'latitude': ..., 'longitude': ...}
    rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.service_type}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    rating_value = models.IntegerField(default=5)  # 1 to 5 scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating_value} for {self.service_provider.username} by {self.user.username}"
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} by {self.user.username} to {self.service_provider.username}"

class Todo(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    isdone = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:20]