from rest_framework import serializers
from ..models import Minutes

class MeetingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Minutes
        fields = ['pk','title','date','minutes']