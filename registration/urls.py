from django.urls import path
from .views import UserSignIn

urlpatterns = [
    # API urls
    path('api/sign_in', UserSignIn.as_view()),
]
