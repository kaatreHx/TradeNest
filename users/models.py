from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        if not phone_number:
            raise ValueError('Phone number is required')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, phone_number, password, **extra_fields)

def user_profile_image_path(instance, filename):
    return f'profile_images/user_{instance.id}/{filename}'

def user_kyc_document_path(instance, filename):
    return f'kyc_documents/user_{instance.user.id}/{filename}'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True) #For user banned
    is_staff = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False) #Vendor->False is customer
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name']
    
    def __str__(self):
        return self.email

class UserKYC(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    nationality = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to=user_profile_image_path, default='profile_images/default.png', blank=True, null=True)

    # Address info
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    # Identity documents
    document_type = models.CharField(max_length=50, choices=[('nid', 'National ID'), ('passport', 'Passport'), ('license', 'Driver License')])
    document_number = models.CharField(max_length=100, unique=True)
    document_front = models.ImageField(upload_to=user_kyc_document_path, blank=True, null=True)
    document_back = models.ImageField(upload_to=user_kyc_document_path, blank=True, null=True)

    # Verification status
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"KYC for {self.user.name}"



