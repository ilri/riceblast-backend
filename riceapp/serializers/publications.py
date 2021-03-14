from rest_framework import serializers
from ..models import Publications

class PublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publications
        fields = ['pk','title','date','description','publication']