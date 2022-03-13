from django.urls import path
from .views import UserSignUp, UserSignIn

urlpatterns = [
    # API urls
    path('api/sign_up/', UserSignUp.as_view()),
    path('api/sign_in/', UserSignIn.as_view()),
]
