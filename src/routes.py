from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('', include('src.listing.urls')),
    path('users/', include('src.users.urls')),
    path('users-login-jwt/', TokenObtainPairView.as_view()),
    path('users-token-refresh/', TokenRefreshView.as_view()),
]
