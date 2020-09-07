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
from .serializers.people import PeopleSerializer,PeopleUserSerializer 
from .serializers.riceblastlabs import RiceblastlabSerializer
from .serializers.collectionsites import CollectionSiteSerializer,CollectionSitePostSerializer
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
from django.db.models.functions import Upper






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

class UserList(APIView):
    ''' API class based view for handling User Information'''
    def post(self, request,format=None):
        user_info = {
            'username':request.data.get('username'),
            'email':request.data.get('email'),
            'password':request.data.get('password'),
        }
        people_info = {
            'full_name':request.data.get('full_name'),
            'telephone_number':request.data.get('telephone_number'),
            'lab':request.data.get('lab'),
            'designation':request.data.get('designation'),
        }
        
        user_serializer = UserSerializerWithToken(data=user_info)

        # CHECK IF CREDENTIALS EXIST
        check_username = User.objects.filter(username=user_info['username'])
        check_email = User.objects.filter(email=user_info['email'])
        if len(check_username) is 0:
            if len(check_email) is 0:
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    people_info['user'] = user.pk
                    print(user_info,people_info)

                    people_serializer = PeopleSerializer(data=people_info)
                    if people_serializer.is_valid():
                        # people_serializer.user = user
                        people_serializer.save()
                        return Response({"message":'User has been successfully registered. You can add another user above.'},status=status.HTTP_201_CREATED)
                    return Response({"message":'One/More of your Professional Information Fields has an Error.'},status=status.HTTP_400_BAD_REQUEST)                    
                return Response({"message":'One or more fields has the wrong data type.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":'Email already Exists. Please use a different email.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message":'Username already Exists. Please use a different username.'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self,request,username,format=None):
        print(username)
        user = User.objects.get(username=username)
        person = People.objects.get(user=user)
        user.delete()
        person.delete()
        return Response(status=status.HTTP_200_OK)




@api_view(['PUT'])
def activate_user(request):
    '''
    Admin function for activating/deactivating user accounts based on request action.
    '''
    username = request.data.get('username')
    action = request.data.get('action')
    user = User.objects.get(username=username)
    print(action == 'activate')
    if action == 'activate':
        user.is_active = True
        user.save()
        return Response({'message':'User has been Activated.'},status=status.HTTP_200_OK)
    else:
        user.is_active = False
        user.save()
        return Response({'message':'User has been Deactivated.'},status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data.
    """
    people_data = People.objects.get(user=request.user.pk)
    serializer = PeopleUser(people_data)
    return Response(serializer.data)        
@api_view(['GET'])
def all_people(request):
    '''
    Get all people in the system.
    '''
    people = People.objects.all()
    serializer = PeopleUserSerializer(people, many=True)
    return Response(serializer.data)










class RiceBlastLabList(APIView):
    '''Class based view for Labs'''

    def get(self,request,format=None):
        riceblastlabs = RiceBlastLab.objects.all().order_by('pk')
        serializer = RiceblastlabSerializer(riceblastlabs, many=True)
        return Response(serializer.data) 
    
    def post(self,request,format=None):
        print(request.data)
        new_lab = { 
            'lab_id':request.data.get('lab_id'),
            'lab_name':request.data.get('lab_name'),
            'country':request.data.get('country'),
            'institution':request.data.get('institution'),
            'principal_investigator':request.data.get('principal_investigator'),
        }
        serializer = RiceblastlabSerializer(data=new_lab)
        convert_to_uppercase = new_lab['lab_id'].upper()
        print(convert_to_uppercase)
        lab_id_exists = RiceBlastLab.objects.filter(lab_id=convert_to_uppercase)
        if len(lab_id_exists) == 0:
            if serializer.is_valid():
                serializer.save()
            else:        
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Lab ID already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self,request, pk,format=None):
        print(pk)
        lab = RiceBlastLab.objects.get(pk=pk)
        lab.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        print(request.data)
        lab_id = request.data.get('pk')
        lab = RiceBlastLab.objects.get(pk=lab_id)
        if lab.lab_id is not request.data.get('lab_id'):
            lab.lab_id = request.data.get('lab_id')
        if lab.lab_name is not request.data.get('lab_name'):
            lab.lab_name = request.data.get('lab_name')
        if lab.country is not request.data.get('country'):
            lab.country = request.data.get('country')                                                
        if lab.institution is not request.data.get('institution'):
            lab.institution = request.data.get('institution')  
        if lab.principal_investigator is not request.data.get('principal_investigator'):
            lab.principal_investigator = request.data.get('principal_investigator')                        
        lab.save()

        return Response(status=status.HTTP_200_OK)
###############################################333333333######
##################################################################3
#################################################################


class CollectionSiteList(APIView):
    '''API Class view for Handling requests to Fungal Collection Sites'''

    def get(self,request,format=None):
        collection_sites = FungalCollectionSite.objects.all()
        serializer = CollectionSiteSerializer(collection_sites, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        print(request.data)

        new_site = {
            'name':request.data.get('name'),
            'type':request.data.get('type'),
            'latitude':request.data.get('latitude'),
            'longitude':request.data.get('longitude'),
            'country':request.data.get('country'),
        }

        serializer = CollectionSitePostSerializer(data=new_site)

        project = None
        if request.data.get('project') is not None:
            project = Project.objects.get(pk=request.data.get('project'))

        person = None
        if request.data.get('person') is not None:
            person = People.objects.get(pk=request.data.get('person'))

        if serializer.is_valid():
            print('yes')
            site = serializer.save()
            site.project = project
            site.person = person
            site.save()
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,format=None):
        print(request.data)
        site_id = request.data.get('pk')
        site = FungalCollectionSite.objects.get(pk=site_id)
        if site.name is not request.data.get('name'):
            site.name = request.data.get('name')
        if site.type is not request.data.get('type'):
            site.type = request.data.get('type')
        if site.longitude is not request.data.get('longitude'):
            site.longitude = request.data.get('longitude')
        if site.latitude is not request.data.get('latitude'):
            site.latitude = request.data.get('latitude')  
        if site.country is not request.data.get('country'):
            site.country = request.data.get('country')                                                
        if site.project is not request.data.get('project') and isinstance(request.data.get('person'),int):
            project = Project.objects.get(pk=request.data.get('project'))
            site.project = project 
        if site.person is not request.data.get('person') and isinstance(request.data.get('person'),int):
            person = People.objects.get(pk=request.data.get('person'))
            site.person = person                        
        site.save()
        return Response(status=status.HTTP_200_OK)
    
    def delete(self,request,pk,format=None):
        site = FungalCollectionSite.objects.get(pk=pk)
        print(site)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsolateList(APIView):
    def get(self,request,format=None):
        isolates = Isolate.objects.all().order_by('pk')
        serializer = IsolateSerializer(isolates, many=True)
        return Response(serializer.data)  

    def post(self,request,format=None):
        print(request.data)
        # ADD USER - PERSON REGISTERS PK/ID
        new_isolate = {
            'isolate_id':request.data.get('isolate_id'),
            'isolate_name':request.data.get('isolate_name'),
            'taxa_name':request.data.get('taxa_name'),
            'date_collected':request.data.get('date_collected'),
            'date_isolated':request.data.get('date_isolated'),
            'country':request.data.get('country'),
            'host_genotype':request.data.get('host_genotype'),
            'collection_site':request.data.get('collection_site'),
        }

        serializer = IsolateSerializer(data=new_isolate)

        person = None
        if request.data.get('person') is not None:
            person = People.objects.get(pk=request.data.get('person'))

        if serializer.is_valid():
            isolate = serializer.save()
            isolate.person = person
            isolate.save()
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

    def put(self,request,format=None):
        print(request.data)
        isolate = Isolate.objects.get(pk=request.data.get('pk'))
        if isolate.isolate_id is not request.data.get('isolate_id'):
            isolate.isolate_id = request.data.get('isolate_id')
        if isolate.isolate_name is not request.data.get('isolate_name'):
            isolate.isolate_name = request.data.get('isolate_name')
        if isolate.taxa_name is not request.data.get('taxa_name'):
            isolate.taxa_name = request.data.get('taxa_name')
        if isolate.tissue_type is not request.data.get('tissue_type'):
            isolate.tissue_type = request.data.get('tissue_type') 
        if isolate.date_collected is not request.data.get('date_collected'):
            isolate.date_collected = request.data.get('date_collected') 
        if isolate.tissue_type is not request.data.get('tissue_type'):
            isolate.tissue_type = request.data.get('tissue_type') 
        if isolate.date_isolated is not request.data.get('date_isolated'):
            isolate.date_isolated = request.data.get('date_isolated')                                      
        if isolate.country is not request.data.get('country'):
            isolate.country = request.data.get('country') 
        if isolate.host_genotype is not request.data.get('host_genotype'):
            isolate.host_genotype = request.data.get('host_genotype')                                                   
        if isolate.person is not request.data.get('person') and isinstance(request.data.get('person'),int):
            person = People.objects.get(pk=request.data.get('person'))
            isolate.person = person                        
        isolate.save()    
        return Response(status=status.HTTP_200_OK)


    def delete(self,request,pk,format=None):
        isolate = Isolate.objects.get(pk=pk)
        print(isolate)
        isolate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    return Response(serializer.data) 

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
