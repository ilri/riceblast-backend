from rest_framework import serializers
from ..models import People
from django.contrib.auth.models import User

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['full_name','telephone_number']
        
