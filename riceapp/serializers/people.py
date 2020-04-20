from rest_framework import serializers
from ..models import People
from django.contrib.auth.models import User

class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = ['user','full_name','telephone_number','designation','lab']
        

class PeopleUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()

    def get_user(self,person):
        return {
            'pk':person.user.pk,
            "email":person.user.email,
            "username":person.user.username,
            "is_active":person.user.is_active,
        }
    def get_lab(self,person):
        if person.lab is not None: 
            return person.lab.lab_name
    class Meta:
        model = People
        fields = ['user','full_name','telephone_number','designation','lab']
        