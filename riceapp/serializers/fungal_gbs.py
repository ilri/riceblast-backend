from rest_framework import serializers
from ..models import FungalGBS


class FungalGBSSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()


    def get_person(self, fungal_gbs):
        if fungal_gbs.person is not None:
            return fungal_gbs.person.full_name
        return 'Unknown' 


    def get_lab(self, fungal_gbs):
        if fungal_gbs.lab is not None:
            return fungal_gbs.lab.lab_name
        return 'Unknown' 
               
                    
    class Meta:
        model = FungalGBS
        fields = ['fungal_gbs_name','person','lab','gbs_dataset']