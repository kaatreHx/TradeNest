from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BrowseViewSet, ListingViewSet, ImageViewSet, CartViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'create-listing', ListingViewSet, basename='create-listing')
router.register(r'images', ImageViewSet, basename='images')
router.register(r'cart', CartViewSet, basename='cart')
urlpatterns = [
    path('browse/', BrowseViewSet.as_view(), name='browse'),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)