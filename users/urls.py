from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, RegisterView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)