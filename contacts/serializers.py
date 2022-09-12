from rest_framework import serializers
from .models import Person
from registration.models import AppUser

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'phone1', 'phone2', 'phone3', 'email', 'slug']

class PersonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'email', 'phone1', 'phone2', 'phone3', 'slug']

class AppUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['full_name', 'email', 'slug']
