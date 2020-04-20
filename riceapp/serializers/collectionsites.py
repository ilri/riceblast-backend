from rest_framework import serializers
from ..models import FungalCollectionSite

class CollectionSiteSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()

    def get_project(self,collection_site):
        if collection_site.project is not None:
            return collection_site.project.project_name
        return None

    def get_person(self,collection_site):
        if collection_site.person is not None:
            return collection_site.person.full_name
        return None
        
    class Meta:
        model = FungalCollectionSite
        fields = ('pk','name','type','latitude','longitude','country','project','person')

class CollectionSitePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FungalCollectionSite
        fields = ('pk','name','type','latitude','longitude','country')