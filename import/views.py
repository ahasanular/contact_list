import time

import numpy as np
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from contacts.models import Person
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import ImportContactSerializer
from threading import Thread
from io import StringIO             # for proccess csv file
import pandas as pd
# end of import


def save_contacts_later(data, user):
    for index, row in data.iterrows():
        person = Person()
        person.user = user
        person.name = row['Name']
        person.phone1 = row['Phone 1 - Value']

        if 'E-mail 1 - Value' in row:
            person.email = row['E-mail 1 - Value']
        else:
            person.email = ""
        if 'Phone 2 - Value' in row:
            person.phone2 = row['Phone 2 - Value']
        if 'Phone 3 - Value' in row:
            person.phone3 = row['Phone 3 - Value']

        person.save()

def save_contacts_thread(data, user):
    thread = Thread(target=save_contacts_later, args=(data, user))
    thread.start()

def save_contacts(file, user):
    feedback = {}
    try:
        csvf = StringIO(file.read().decode())

        hello = pd.read_csv(csvf, header=0)
        hello = hello.replace(np.nan, '', regex=True)

        person_list = []

        i = 0
        for index, row in hello.iterrows():
            if i == 20:
                break
            person = Person()
            person.user = user
            person.name = row['Name']
            person.phone1 = row['Phone 1 - Value']

            if 'E-mail 1 - Value' in row:
                person.email = row['E-mail 1 - Value']
            else:
                person.email = ""
            if 'Phone 2 - Value' in row:
                person.phone2 = row['Phone 2 - Value']
            if 'Phone 3 - Value' in row:
                person.phone3 = row['Phone 3 - Value']

            person.save()

            i = i + 1

        df1 = hello.drop(hello.index[:20])

        save_contacts_thread(df1, user)

        feedback['message'] = "Contacts Imported Successfully"
        feedback['status'] = HTTP_200_OK
        return feedback

    except Exception as ex:
        feedback['message'] = str(ex)
        feedback['status'] = HTTP_400_BAD_REQUEST
        return feedback


class ImportContactApi(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = ImportContactSerializer

    def post(self, request, *args, **kwargs):
        feedback = {}
        try:
            data = request.data
            user = request.user

            if 'contacts_file' not in data or data['contacts_file'] == "" or not request.FILES['contacts_file']:
                feedback['message'] = "Importing file not found !"
                feedback['status'] = HTTP_204_NO_CONTENT
                return Response(feedback)

            file_name = data['contacts_file'].name
            file_name = file_name.split('.')

            if file_name[len(file_name)-1] == 'csv':
                save_contacts(data['contacts_file'], user)

                feedback['message'] = "Successful"
                feedback['status'] = HTTP_200_OK
                return Response(feedback)
            else:
                feedback['message'] = "Only csv file supported"
                feedback['status'] = HTTP_400_BAD_REQUEST
                return Response(feedback)

        except Exception as ex:
            feedback['message'] = str(ex)
            feedback['status'] = HTTP_400_BAD_REQUEST
            return Response(feedback)

# class ImportContactApi(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ImportContactSerializer
#     def post(self, request, *args, **kwargs):
#         feedback = {}
#         try:
#             file = request.FILES.get('contacts_file')
#             user = request.user
#             reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
#
#             data = list(reader)
#
#             print("<<<<<<<<<<<<<TESTING>>>>>>>>>>>>")
#             print(data)
#
#             serializer = self.serializer_class(data=data, many=True)
#
#             serializer.initial_data()
#             print("row['Name']")
#
#             person_list = []
#             for row in serializer.data:
#                 print(row['Name'])
#
#             # print("testing person_list")
#             # print(person_list)
#
#             # Person.objects.bulk_create(person_list)
#
#             feedback['message'] = "successfully imported contacts"
#             feedback['status'] = HTTP_200_OK
#             return Response(feedback)
#
#         except Exception as ex:
#             feedback['message'] = str(ex)
#             feedback['status'] = HTTP_400_BAD_REQUEST
#             return Response(feedback)