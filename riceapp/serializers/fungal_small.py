from rest_framework import serializers
from ..models import FungalSmallDnaFragmentsSequence


class FungalSmallSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()
    isolate = serializers.SerializerMethodField()

    def get_person(self, fungal_small):
        if fungal_small.person is not None:
            return fungal_small.person.full_name
        return 'Unknown' 

    def get_lab(self, fungal_small):
        if fungal_small.lab is not None:
            return fungal_small.lab.lab_name
        return 'Unknown' 


    def get_isolate(self, fungal_small):
        if fungal_small.isolate is not None:
            return fungal_small.isolate.isolate_name
        return 'Unknown'                
          
    class Meta:
        model = FungalSmallDnaFragmentsSequence
        fields = ['isolate','taxa_name','sequence_id','description','sequence_data',
                'chromosome_id','chromosome_site_id','loci_id','person','lab','target_gene']