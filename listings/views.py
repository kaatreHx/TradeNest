from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Listing, ListingImage, Cart
from .serializers import ListingSerializer, ListingImageSerializer, CartSerializer
from .pagination import CustomPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
import django_filters

class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price', 'title', 'location', 'is_sold']
    search_fields = ['category', 'price', 'title', 'location', 'is_sold']

    def get_queryset(self):
        return Listing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BrowseViewSet(ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price', 'title', 'location', 'is_sold']
    search_fields = ['category', 'price', 'title', 'location', 'is_sold']

    def get_queryset(self):
        return Listing.objects.all()

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ListingImageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['listing']
    search_fields = ['listing']

    def get_queryset(self):
        return ListingImage.objects.filter(listing=self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['listing']
    search_fields = ['listing']

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)