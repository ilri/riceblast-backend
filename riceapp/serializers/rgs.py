from rest_framework import serializers
from ..models import RiceGeneScreenResult
from django.contrib.auth.models import User

class RGSSerializer(serializers.ModelSerializer):
    rice_genotype = serializers.SerializerMethodField()
    rice_gene = serializers.SerializerMethodField()
    
    def get_rice_genotype(self, rgs):
        if rgs.rice_genotype is not None:
            return rgs.rice_genotype.name
        return 'Unknown'
    def get_rice_gene(self,rgs):
        if rgs.rice_gene is not None:
            return rgs.rice_gene.name
        return 'Unknown'
        
    class Meta:
        model = RiceGeneScreenResult
        fields = ['pk','rice_genotype','rice_gene','pcr_results','replicate_id','sample_id']

class RGSPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiceGeneScreenResult
        fields = ('pk','pcr_results','replicate_id','sample_id')