from rest_framework import serializers
from ..models import Isolate

class IsolateSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()
    date_isolated = serializers.SerializerMethodField()
    date_collected = serializers.SerializerMethodField()


    def get_person(self, isolate):
        if isolate.person is not None:
            return isolate.person.full_name
        return ''
    def get_date_isolated(self, isolate):
        if isolate.date_isolated is not None:
            return isolate.date_isolated
        return ''

    def get_date_collected(self, isolate):
        if isolate.date_collected is not None:
            return isolate.date_collected
        return ''
    class Meta:
        model = Isolate
        fields = ('pk','isolate_id', 'isolate_name','taxa_name','tissue_type',
                'date_collected','date_collected','date_isolated', 'country', 
                'host_genotype', 'collection_site' ,'person')