from rest_framework import serializers
from ..models import RiceGene

class RiceGenesSerializer(serializers.ModelSerializer):


    class Meta:
        model = RiceGene
        fields = ('name','chromosome_id','marker','donor_line','resistance_type','reference')