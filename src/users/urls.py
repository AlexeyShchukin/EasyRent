from django.urls import path

from src.users.views import RegisterView, LoginUserAPIView, LogoutUserAPIView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout')
]
