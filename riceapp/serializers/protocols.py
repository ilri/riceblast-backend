from rest_framework import serializers
from ..models import Protocol


class ProtocolSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()


    def get_person(self, protocol):
        if protocol.person is not None:
            return protocol.person.full_name
        return 'Unknown' 


    def get_lab(self, protocol):
        if protocol.lab is not None:
            return protocol.lab.lab_name
        return 'Unknown' 
               
                    
    class Meta:
        model = Protocol
        fields = ['name','protocol_id','key_reference','protocol','person',
                'lab','protocol_modified','related_protocols']