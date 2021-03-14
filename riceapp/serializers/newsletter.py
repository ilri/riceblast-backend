from rest_framework import serializers
from ..models import Newsletters

class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletters
        fields = ['pk','title','date','description','newsletter']