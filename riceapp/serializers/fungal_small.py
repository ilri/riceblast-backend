from rest_framework import serializers
from ..models import FungalSmallDnaFragmentsSequence


class FungalSmallSerializer(serializers.ModelSerializer):

    person = serializers.SerializerMethodField()

    def get_person(self, fungal_small):
        if fungal_small.person is not None:
            return fungal_small.person.full_name
        return 'Unknown' 

    class Meta:
        model = FungalSmallDnaFragmentsSequence
        fields = [
            'pk',
            'activity_name',
            'fungal_gene_name',
            'fungal',
            'fungal_gene_sequence',
            'date_of_sequence',
            'project_name',
            'loci_id',
            'person',
            'target_gene' 
        ]

