from rest_framework import serializers
from ..models import Isolate

class IsolateSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    def get_person(self, isolate):
        if isolate.person is not None:
            return isolate.person.full_name
        return 'Unknown'

    class Meta:
        model = Isolate
        fields = ('isolate_id', 'isolate_name','taxa_name','tissue_type',
                'date_collected','date_collected','date_isolated', 'country', 
                'host_genotype', 'collection_site' ,'person')