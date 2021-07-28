from rest_framework import serializers
from ..models import FungalGeneScreenResult


class FGSSerializer(serializers.ModelSerializer):
    isolate = serializers.SerializerMethodField()

    def get_isolate(self, rgs):
        if rgs.isolate is not None:
            return rgs.isolate.isolate_id
        return 'Unknown'    
    class Meta:
        model = FungalGeneScreenResult
        fields = ['pk','isolate','fungal_gene','pcr_results','replicate_id','sample_id']