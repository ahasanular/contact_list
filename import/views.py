import numpy as np
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_406_NOT_ACCEPTABLE
from contacts.models import Person
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import ImportContactSerializer

# for proccess csv file
from io import StringIO
import pandas as pd

def import_from_csv(file, user):
    feedback = {}
    try:
        csvf = StringIO(file.read().decode())
        print("csv IO decod check")

        hello = pd.read_csv(csvf, header=0)
        print("panda read checked")
        hello = hello.replace(np.nan, '', regex=True)
        # print("nan replce checked")

        person_list = []
        for index, row in hello.iterrows():
            print("testing index")
            person = Person()
            print("person create checked")
            person.user = user
            print("user assign checked")
            person.name = row['Name']
            print("name assign checked")
            person.phone1 = row['Phone 1 - Value']
            print("Phone 1 assigned")

            if 'E-mail 1 - Value' in row:
                person.email = row['E-mail 1 - Value']
            else:
                person.email = ""
            if 'Phone 2 - Value' in row:
                person.phone2 = row['Phone 2 - Value']
            if 'Phone 3 - Value' in row:
                person.phone3 = row['Phone 3 - Value']

            print("person[index]")
            print(person)
            # person_list.append(person)
            person.save()

        print("Final TEST --------------------->>>>>>>>>>>>>>>>>>>>>>>>")
        print(person_list)

        # serializer = self.serializer_class(data=person_list, many=True)
        # serializer.is_valid()
        # serializer.validated_data
        # serializer.save()

        # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SERIALIZER>DATA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(person_list)
        # Person.objects.bulk_create(person_list, ignore_conflicts=True)

        feedback['message'] = "Contacts Imported Successfully"
        feedback['status'] = HTTP_200_OK
        return feedback

    except Exception as ex:
        feedback['message'] = str(ex)
        feedback['status'] = HTTP_400_BAD_REQUEST
        return feedback


class ImportContactApi(CreateAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = ImportContactSerializer
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
                feedback = import_from_csv(data['contacts_file'], user)
                return Response(feedback)
            else:
                feedback['message'] = "Contacts Imported Successfully"
                feedback['status'] = HTTP_200_OK
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