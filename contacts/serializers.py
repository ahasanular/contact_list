from .models import Person
from rest_framework import serializers

class PersonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'email', 'phone', 'slug']
