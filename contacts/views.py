from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer

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
