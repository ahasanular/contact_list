from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer
import json

def contactList(request):
    return render(request, 'index.html')


#api
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

class contact_list_api(ListAPIView):
    permission_classes = []
    def get(self, request):
        data = Person.objects.filter().all()
        data = PersonSerializer(data, many=True).data
        return Response(data)

class contact_list_api(CreateAPIView):
    permission_classes = []
    def get(self, request):
        data = Person.objects.filter().all()
        data = PersonSerializer(data, many=True).data
        return Response(data)

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
                person.name =