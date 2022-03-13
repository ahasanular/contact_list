from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer, PersonDetailsSerializer
import json
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated

def contactList(request):
    return render(request, 'index.html')

def details(request, slug):
    return render(request, 'contact_details.html')

def addcontact(request):
    return render(request,'add_contact.html')


#All api
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

class contact_list_api(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Person.objects.filter().all()
        data = PersonSerializer(data, many=True).data
        return Response(data)

class DetailsApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        data_val = Person.objects.filter(slug=slug).first()
        data_val = PersonDetailsSerializer(data_val).data
        return Response(data_val)

class contact_edit_api(CreateAPIView):
    permission_classes = []
    def put(self, request, slug):
        try:
            data = json.loads(request.body)

            person = Person.objects.filter(slug=slug).first()

            if not person:
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "Person was not found !"
                return Response(feedback)
            else:
                person.email = data['email']
                person.name = data['name']
                person.phone = data['phone']
                person.save()

                feedback = {}
                feedback['status'] = HTTP_200_OK
                feedback['message'] = "All details updated !"
                return Response(feedback)
        except Exception as ex:
            feedback = {}
            feedback['status'] = HTTP_400_BAD_REQUEST
            feedback['message'] = str(ex)
            return Response(feedback)


class Add_contact_api(CreateAPIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        try:
            #data= request.data
            data= json.loads(request.body)
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
            result = {}
            result['status'] = HTTP_200_OK
            result['message'] = "success"
            return Response(result)

        except Exception as ex:
            result = {}
            result['status'] = HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)

