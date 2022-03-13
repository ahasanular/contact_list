from django.urls import path
from .views import UserSignUp, UserSignIn, sign_up, sign_in, sign_out, root

urlpatterns = [
    # API urls
    path('api/sign_up/', UserSignUp.as_view()),
    path('api/sign_in/', UserSignIn.as_view()),

    # function based views
    path('', root),
    path('signin/', sign_in),
    path('signup/', sign_up),
    path('signout/', sign_out),
]
