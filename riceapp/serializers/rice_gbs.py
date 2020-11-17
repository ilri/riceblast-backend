from rest_framework import serializers
from ..models import RiceGBS


class RiceGBSSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()


    def get_person(self, rice_gbs):
        if rice_gbs.person is not None:
            return rice_gbs.person.full_name
        return 'Unknown' 


    def get_lab(self, rice_gbs):
        if rice_gbs.lab is not None:
            return rice_gbs.lab.lab_name
        return 'Unknown' 
               
                    
    class Meta:
        model = RiceGBS
        fields = ['rice_gbs_name','person','lab','gbs_dataset','pk']