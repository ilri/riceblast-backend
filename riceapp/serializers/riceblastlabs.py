from rest_framework import serializers
from ..models import RiceBlastLab

class RiceblastlabSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiceBlastLab
        fields = ('lab_id', 'lab_name','country','institution','principal_investigator')