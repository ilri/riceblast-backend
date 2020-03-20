from rest_framework import serializers
from ..models import PathotypingResults


class PathotypingResultsSerializer(serializers.ModelSerializer):
    rice_genotype = serializers.SerializerMethodField()
    isolate = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()
    lab = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    def get_rice_genotype(self, results):
        if results.rice_genotype is not None:
            return results.rice_genotype.name
        return 'Unknown'    

    def get_isolate(self, results):
        if results.isolate is not None:
            return results.isolate.isolate_name
        return 'Unknown' 

    def get_person(self, results):
        if results.person is not None:
            return results.person.full_name
        return 'Unknown' 

    def get_lab(self, results):
        if results.lab is not None:
            return results.lab.lab_name
        return 'Unknown' 

    def get_project(self, results):
        if results.project is not None:
            return results.project.project_name
        return 'Unknown'                       
          
    class Meta:
        model = PathotypingResults
        fields = ['replicate_id','sample_id','stock_id','date_inoculated','date_scored',
                'date_planted','disease_score','tray','rice_genotype','isolate','person','lab','project']
        

        




     
    


