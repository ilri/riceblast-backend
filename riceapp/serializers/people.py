from rest_framework import serializers
from ..models import People
from django.contrib.auth.models import User

class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = ['user','full_name','telephone_number','designation','lab']
        

class PeopleUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    

    def get_user(self,person):
        return {
            "email":person.user.email,
            "username":person.user.username,
        }

    class Meta:
        model = People
        fields = ['user','full_name','telephone_number','designation','lab']
        