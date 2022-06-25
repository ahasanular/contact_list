from rest_framework import serializers
from contacts.models import Person

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField

class SaveFileSerializer(serializers.Serializer):

    class Meta:
        model = Person
        fields = "__all__"

# class ImportContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = ['user', 'name', 'email', 'phone1', 'phone2', 'phone3']

# class ImportContactSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Person
#         fields = ['user', 'name', 'phone1', 'email', 'phone2', 'phone3']


class ImportContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

