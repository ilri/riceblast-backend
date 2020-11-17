from rest_framework import serializers
from ..models import Protocol


class ProtocolSerializer(serializers.ModelSerializer):
              
                    
    class Meta:
        model = Protocol
        fields = ['name','protocol','pk']