from rest_framework import serializers
from .models import CustomUser, UserKYC, UserRating 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'password']
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = '__all__'


