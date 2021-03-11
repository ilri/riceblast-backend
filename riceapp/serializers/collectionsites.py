from rest_framework import serializers
from ..models import FungalCollectionSite

class CollectionSiteSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()


    def get_person(self,collection_site):
        if collection_site.person is not None:
            return collection_site.person.full_name
        return None
        
    class Meta:
        model = FungalCollectionSite
        fields = ('pk','name','type','latitude','longitude','country','person')

