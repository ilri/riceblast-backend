from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password
from .serializers.users import UserSerializer,UserSerializerWithToken
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from .serializers.people import PeopleSerializer 
from .serializers.riceblastlabs import RiceblastlabSerializer
from .serializers.collectionsites import CollectionSiteSerializer
from .serializers.isolates import IsolateSerializer
from .serializers.rice_genotypes import RiceGenotypeSerializer
from .serializers.rice_genes import RiceGenesSerializer
from .serializers.rgs import RGSSerializer
from .serializers.fgs import FGSSerializer
from .serializers.pathotyping_results import PathotypingResultsSerializer
from .serializers.vcg_groups import VCGGroupSerializer
from .serializers.rice_small import RiceSmallSerializer
from .serializers.fungal_small import FungalSmallSerializer
from .serializers.vcg_test_results import VCGTestResultsSerializer
from .serializers.protocols import ProtocolSerializer
from .serializers.rice_gbs import RiceGBSSerializer
from .serializers.fungal_gbs import FungalGBSSerializer







# Create your views here. 


class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data.
    """
    people_data = People.objects.get(user=request.user.pk)
    serializer = PeopleSerializer(people_data)
    return Response(serializer.data)        

@api_view(['GET'])
def riceblastlabs(request):
    '''
    All Rice Blast Labs.
    '''
    riceblastlabs = RiceBlastLab.objects.all()
    serializer = RiceblastlabSerializer(riceblastlabs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fungal_collection_sites(request):
    '''
    All Fungal Collection Sites.
    '''
    collection_sites = FungalCollectionSite.objects.all()
    serializer = CollectionSiteSerializer(collection_sites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def isolates(request):
    '''
    All Isolates.
    '''
    isolates = Isolate.objects.all()
    serializer = IsolateSerializer(isolates, many=True)
    return Response(serializer.data)    


@api_view(['GET'])
def rice_genotypes(request):
    '''
    All Rice Genotypes.
    '''
    rice_genotypes = RiceGenotype.objects.all()
    serializer = RiceGenotypeSerializer(rice_genotypes, many=True)
    return Response(serializer.data)     

@api_view(['GET'])
def rice_genes(request):
    '''
    All Rice Genes.
    '''
    rice_genes = RiceGene.objects.all()
    serializer = RiceGenesSerializer(rice_genes, many=True)
    return Response(serializer.data) \

@api_view(['GET'])
def rgs(request):
    '''
    All Rice Gene Screen Results.
    '''
    rgs_results = RiceGeneScreenResult.objects.all()
    serializer = RGSSerializer(rgs_results, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fgs(request):
    '''
    All FungaL Gene Screen Results.
    '''
    fgs_results = FungalGeneScreenResult.objects.all()
    serializer = FGSSerializer(fgs_results, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pathotyping_results(request):
    '''
    All Pathotyping Results.
    '''
    results = PathotypingResults.objects.all()
    serializer = PathotypingResultsSerializer(results, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vcg_groups(request):
    '''
    All VCG Groups.
    '''
    groups = VcgGroup.objects.all()
    serializer = VCGGroupSerializer(groups, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def rice_small(request):
    '''
    All Rice Small DNA Fragments.
    '''
    rice_small = RiceSmallDnaFragmentsSequence.objects.all()
    serializer = RiceSmallSerializer(rice_small, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fungal_small(request):
    '''
    All Fungal Small DNA Fragments.
    '''
    fungal_small = FungalSmallDnaFragmentsSequence.objects.all()
    serializer = FungalSmallSerializer(fungal_small, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vcg_test_results(request):
    '''
    All VCG Test Results.
    '''
    results = VCGTestResults.objects.all()
    serializer = VCGTestResultsSerializer(results, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def protocol(request):
    '''
    All Protocols.
    '''
    protocols = Protocol.objects.all()
    serializer = ProtocolSerializer(protocols, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def rice_gbs(request):
    '''
    All Rice GBS.
    '''
    results = RiceGBS.objects.all()
    serializer = RiceGBSSerializer(results, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fungal_gbs(request):
    '''
    All Fungal GBS.
    '''
    results = FungalGBS.objects.all()
    serializer = FungalGBSSerializer(results, many=True)
    return Response(serializer.data)    
