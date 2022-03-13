from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.utils import json
from .models import AppUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect


# Create your views here.

def signout(request):
    response = HttpResponseRedirect('/access/')
    response.delete_cookie('access')
    response.delete_cookie('user_name')
    return response


# APIs
class UserSignIn(generics.ListAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        result = {}
        try:
            data = json.loads(request.body)
            print(data)
            if 'email' not in data or data['email']=='':
                result['message']="Email can not be null."
                result['Error']="Email"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            if 'password' not in data or data['password'] == '':
                result['message'] = "Password can not be null."
                result['Error'] = "Password"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=data['email']).first()
            if not user:
                result = {
                    'message': 'Please create a account'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            elif not user.is_active:
                result = {
                    'message': 'Please activate your account'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not check_password(data['password'], user.password):
                    result['message'] = "Invalid credentials"
                    return Response(result, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    app_user = AppUser.objects.filter(user=user).first()
                    token = RefreshToken.for_user(user)
                    data = {
                        'user_name': user.username,
                        'access': str(token.access_token),
                        'token': str(token),
                        'status': status.HTTP_200_OK
                    }
                    return Response(data)
        except Exception as e:
            result = {}
            result['status'] = status.HTTP_400_BAD_REQUEST
            result['message'] = str(e)
            return Response(result)
