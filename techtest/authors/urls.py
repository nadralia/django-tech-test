from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path("authors/", RegistrationAPIView.as_view()),
    path("authors/login/", LoginAPIView.as_view()),
    path('author', UserRetrieveUpdateAPIView.as_view()),
]