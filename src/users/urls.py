from django.urls import path

from src.users.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
]
