from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response 
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import CustomUser, UserRating 
from .serializers import RegistrationSerializer, CustomUserSerializer, UserRatingSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .pagination import CustomPagination
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def post(self, request):
        id = request.data.get('id')
        password = request.data.get('password')

        if not id or not password:
            return Response({
                'detail': 'Id and password required'
            }, status =  status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.filter(email=id).first()
        if not user:
            user = CustomUser.objects.filter(phone_number=id).first()
        
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':{
                    'id': user.id,
                    'name': user.name, 
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'is_vendor': user.is_vendor
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'detail': 'Invalid credentials'
        }, status = status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(CreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user':{
                'id': user.id,
                'name': user.name, 
                'email': user.email,
                'phone_number': user.phone_number,
                'is_vendor': user.is_vendor
            }
        }, status = status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['get', 'put', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'phone_number']
    pagination_class = CustomPagination

class UserRatingViewSet(viewsets.ModelViewSet):
    serializer_class = UserRatingSerializer
    queryset = UserRating.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__name', 'user__email', 'user__phone_number']
    pagination_class = CustomPagination
