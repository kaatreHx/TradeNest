from django.contrib import admin
from .models import CustomUser, UserKYC, UserRating

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
        'phone_number',
        'is_staff',
        'last_login',
        'date_joined',
    )

@admin.register(UserKYC)
class UserKYCAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'date_of_birth',
        'gender',
        'nationality',
        'profile_picture',
        'address',
        'city',
        'country',
        'postal_code',
        'document_type',
        'document_number',
        'document_front',
        'document_back',
        'is_verified',
        'submitted_at',
        'verified_at',
    )

    list_filter = ('gender', 'country', 'is_verified', 'submitted_at', 'verified_at')
    
    search_fields = (
    'full_name',
    'document_number',
    'country',
    'city',
    'document_type',
    )

@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'rating',
        'comment',
        'created_at',
        'updated_at',
    )
    list_filter = ('user', 'rating', 'created_at', 'updated_at')
    search_fields = ('user', 'comment')
