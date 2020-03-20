from rest_framework import serializers
from ..models import VCGTestResults


class VCGTestResultsSerializer(serializers.ModelSerializer):

    isolate = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()
    vcg = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    def get_project(self, results):
        if results.project is not None:
            return results.project.project_name
        return 'Unknown' 

    def get_lab(self, results):
        if results.lab is not None:
            return results.lab.lab_name
        return 'Unknown' 


    def get_isolate(self, results):
        if results.isolate is not None:
            return results.isolate.isolate_name
        return 'Unknown'                

    def get_vcg(self, results):
        if results.vcg is not None:
            return results.vcg.vcg_id
        return 'Unknown'                
                    
    class Meta:
        model = VCGTestResults
        fields = ['vcg_test_id','isolate','vcg_tester_id','tester_and_control','tester_complimented_isolate',
                'lab','vcg_replicate_id','vcg','project']