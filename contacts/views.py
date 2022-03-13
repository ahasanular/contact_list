from django.shortcuts import render
from .serializers import PersonDetailsSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Person

# Create your views here.

def details(request, slug):
    return render(request, 'contact_details.html')


class DetailsApi(ListAPIView):
    permission_classes = []
    def get(self, request, slug):
        data_val = Person.objects.filter(slug=slug).first()
        data_val = PersonDetailsSerializer(data_val).data
        return Response(data_val)