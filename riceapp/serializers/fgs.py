from rest_framework import serializers
from ..models import FungalGeneScreenResult


class FGSSerializer(serializers.ModelSerializer):
    rice_genotype = serializers.SerializerMethodField()

    def get_rice_genotype(self, rgs):
        if rgs.rice_genotype is not None:
            return rgs.rice_genotype.name
        return 'Unknown'    
    class Meta:
        model = FungalGeneScreenResult
        fields = ['rice_genotype','fungal_gene','pcr_results','replicate_id','sample_id']