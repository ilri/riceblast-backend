from rest_framework import serializers
from ..models import RiceSmallDnaFragmentsSequence


class RiceSmallSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()
    rice_genotype = serializers.SerializerMethodField()

    def get_person(self, rice_small):
        if rice_small.person is not None:
            return rice_small.person.full_name
        return 'Unknown' 

    def get_lab(self, rice_small):
        if rice_small.lab is not None:
            return rice_small.lab.lab_name
        return 'Unknown' 


    def get_rice_genotype(self, rice_small):
        if rice_small.rice_genotype is not None:
            return rice_small.rice_genotype.name
        return 'Unknown'                
          
    class Meta:
        model = RiceSmallDnaFragmentsSequence
        fields = ['rice_genotype','taxa_name','sequence_id','description','sequence_data',
                'chromosome_id','chromosome_site_id','loci_id','person','lab','target_gene']
        