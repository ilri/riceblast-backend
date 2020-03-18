from rest_framework import serializers
from ..models import FungalCollectionSite

class CollectionSiteSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()

    def get_project(self,collection_site):
        if collection_site.project is not None:
            return collection_site.project.project_name
        return 'Unknown'

    def get_person(self,collection_site):
        if collection_site.person is not None:
            return collection_site.person.full_name
        return 'Unknown'
        
    class Meta:
        model = FungalCollectionSite
        fields = ('name','type','latitude','longitude','country','project','person')