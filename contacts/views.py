from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Person
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User
from rest_framework.utils import json


def addcontact(request):
    return render(request,'add_contact.html')

class Add_contact_api(CreateAPIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        try:
            data= request.data
            #data= json.loads(request.body)
            user= request.user
            person = Person()
            if 'name' not  in data or data['name']=='':
                return Response('Please Enter Your Name',status=400)
            if 'phone' not  in data or data['phone']=='':
                return Response('Please Enter Phone Number',status=400)

            person.user= user
            person.name=data['name']
            person.phone=data['phone']
            person.email=data['email']
            person.save()
            return Response('Success')
        except Exception as ex:
            result = {}
            result['status'] = HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)

