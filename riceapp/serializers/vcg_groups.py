from rest_framework import serializers
from ..models import VcgGroup


class VCGGroupSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()
 

    def get_person(self, group):
        if group.person is not None:
            return group.person.full_name
        return 'Unknown' 

    def get_lab(self, group):
        if group.lab is not None:
            return group.lab.lab_name
        return 'Unknown' 

                
          
    class Meta:
        model = VcgGroup
        fields = ['pk','vcg_id','group','person','lab']