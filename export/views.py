from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST
from contacts.models import Person
from registration.models import AppUser
import csv
from django.http import HttpResponse
from io import StringIO

# Create your views here.
def export_contact(request, slug):
    app_user = AppUser.objects.filter(slug=slug).first()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'E-mail 1 - Value', 'Phone 1 - Value', 'Phone 2 - Value', 'Phone 3 - Value'])
    data = Person.objects.filter(is_archived__in=[False], user=app_user.user).all()
    for row in data:
        rowobj = [row.name, row.email, row.phone1, row.phone2, row.phone3]
        writer.writerow(rowobj)
    return response
