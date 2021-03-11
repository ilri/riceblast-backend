from rest_framework import serializers
from ..models import RiceGene

class RiceGenesSerializer(serializers.ModelSerializer):


    class Meta:
        model = RiceGene
        fields = ('pk','name','chromosome_id','marker_type','marker_name','donor_line','resistance_type','reference')

        