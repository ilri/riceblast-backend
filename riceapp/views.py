from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password
from .serializers.users import UserSerializer,UserSerializerWithToken
from django.http import HttpResponseRedirect,HttpResponse
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
from .serializers.rgs import RGSSerializer,RGSPostSerializer
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
import json
from django.conf import settings
from wsgiref.util import FileWrapper




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



class RiceGenotypeList(APIView):
    '''
    All Rice Genotypes.
    '''
    def get(self,request,format=None):
        rice_genotypes = RiceGenotype.objects.all().order_by('pk')
        serializer = RiceGenotypeSerializer(rice_genotypes, many=True)
        return Response(serializer.data)    
  
    def post(self,request,format=None):
        print(request.data)
        new_genotype = {
            'name':request.data.get('name'),
            'rice_genotype_id':request.data.get('rice_genotype_id'),
            'resistance_genes':request.data.get('resistance_genes'),
            'r_gene_sources':request.data.get('r_gene_sources'),
            'susceptible_background':request.data.get('susceptible_background'),
            'accession_number':request.data.get('accession_number'),
            'pedigree':request.data.get('pedigree'),
            'category':request.data.get('category'),
        }
        serializer = RiceGenotypeSerializer(data=new_genotype)
              

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    def put(self,request,format=None):
        print(request.data)
        rice_genotype = RiceGenotype.objects.get(pk=request.data.get('pk'))


        if rice_genotype.name is not request.data.get('name'):
            rice_genotype.name = request.data.get('name')
        if rice_genotype.rice_genotype_id is not request.data.get('rice_genotype_id'):
            rice_genotype.rice_genotype_id = request.data.get('rice_genotype_id')
        if rice_genotype.resistance_genes is not request.data.get('resistance_genes'):
            rice_genotype.resistance_genes = request.data.get('resistance_genes')
        if rice_genotype.r_gene_sources is not request.data.get('r_gene_sources'):
            rice_genotype.r_gene_sources = request.data.get('r_gene_sources')
        # if rgs.rice_genotype is not None:
            # return rgs.rice_genotype.name'r_gene_sources')
        if rice_genotype.susceptible_background is not request.data.get('susceptible_background'):
            rice_genotype.susceptible_background = request.data.get('susceptible_background')
        if rice_genotype.accession_number is not request.data.get('accession_number'):
            rice_genotype.accession_number = request.data.get('accession_number')
        if rice_genotype.pedigree is not request.data.get('pedigree'):
            rice_genotype.pedigree = request.data.get('pedigree')                                                   
        if rice_genotype.category is not request.data.get('category'):
            rice_genotype.category = request.data.get('category')
        rice_genotype.save()    
        return Response(status=status.HTTP_200_OK)


    def delete(self,request,pk,format=None):
        rice_genotype = RiceGenotype.objects.get(pk=pk)
        rice_genotype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RiceGenesList(APIView):
    '''
    All Rice Genes.
    '''
    def get(self,request,format=None):
        rice_genes = RiceGene.objects.all().order_by('pk')
        serializer = RiceGenesSerializer(rice_genes, many=True)
        return Response(serializer.data) 

    def post(self,request,format=None):
        print(request.data)
        new_gene = {
            'name':request.data.get('name'),
            'chromosome_id':request.data.get('chromosome_id'),
            'marker':request.data.get('marker'),
            'donor_line':request.data.get('donor_line'),
            'resistance_type':request.data.get('resistance_type'),
            'reference':request.data.get('reference'),
        }
        serializer = RiceGenesSerializer(data=new_gene)
              

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  


    def put(self,request,format=None):
        print(request.data)
        rice_gene = RiceGene.objects.get(pk=request.data.get('pk'))


        if rice_gene.name is not request.data.get('name'):
            rice_gene.name = request.data.get('name')
        if rice_gene.chromosome_id is not request.data.get('chromosome_id'):
            rice_gene.chromosome_id = request.data.get('chromosome_id')
        if rice_gene.marker is not request.data.get('marker'):
            rice_gene.marker = request.data.get('marker')
        if rice_gene.donor_line is not request.data.get('donor_line'):
            rice_gene.donor_line = request.data.get('donor_line')
        if rice_gene.resistance_type is not request.data.get('resistance_type'):
            rice_gene.resistance_type = request.data.get('resistance_type')
        if rice_gene.reference is not request.data.get('reference'):
            rice_gene.reference = request.data.get('reference')

        rice_gene.save()    
        return Response(status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        rice_gene = RiceGene.objects.get(pk=pk)
        rice_gene.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RGSResultsList(APIView):
    '''
    All Rice Gene Screen Results.
    '''
    def get(self,request,format=None):
        rgs_results = RiceGeneScreenResult.objects.all().order_by('pk')
        serializer = RGSSerializer(rgs_results, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        new_rgs = {
            'pcr_results':request.data.get('pcr_results'),
            'replicate_id':request.data.get('replicate_id'),
            'sample_id':request.data.get('sample_id'),
        }

        serializer = RGSPostSerializer(data=new_rgs)
        rice_genotype = None
        rice_gene = None
        print(request.data)

        if request.data.get('rice_genotype') is not None:
            rice_genotype = RiceGenotype.objects.get(pk=request.data.get('rice_genotype'))             
        if request.data.get('rice_gene') is not None:
            rice_gene = RiceGene.objects.get(pk=request.data.get('rice_gene'))   

        if serializer.is_valid(): 
            rgs = serializer.save()
            rgs.rice_genotype = rice_genotype
            rgs.rice_gene = rice_gene
            print(rgs)
            rgs.save()
            return Response(status=status.HTTP_200_OK)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  


    def put(self,request,format=None):
        print(request.data)
        rgs = RiceGeneScreenResult.objects.get(pk=request.data.get('pk'))

        if( isinstance(request.data.get('rice_genotype'),str)):
            rice_genotype = RiceGenotype.objects.get(name=request.data.get('rice_genotype'))
        else:
            rice_genotype = RiceGenotype.objects.get(pk=request.data.get('rice_genotype'))
        

        if( isinstance(request.data.get('rice_gene'),str) ):
            rice_gene = RiceGene.objects.get(name=request.data.get('rice_gene'))
        else:
            rice_gene = RiceGene.objects.get(pk=request.data.get('rice_gene'))           

        

        if rgs.pcr_results is not request.data.get('pcr_results'):
            rgs.pcr_results = request.data.get('pcr_results')
        if rgs.replicate_id is not request.data.get('replicate_id'):
            rgs.replicate_id = request.data.get('replicate_id')
        if rgs.sample_id is not request.data.get('sample_id'):
            rgs.sample_id = request.data.get('sample_id')
        if rgs.rice_genotype.pk is not request.data.get('rice_genotype'): ##CHANGE
            rgs.rice_genotype = rice_genotype
        if rgs.rice_gene.pk is not request.data.get('rice_gene'): ##CHANGE
            rgs.rice_gene = rice_gene
        rgs.save()    
        return Response(status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        rgs = RiceGeneScreenResult.objects.get(pk=pk)
        rgs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
        
          
class FGSResultsList(APIView):
    '''
    All FungaL Gene Screen Results.
    '''
    def get(self,request,format=None):
        fgs_results = FungalGeneScreenResult.objects.all().order_by('pk')
        serializer = FGSSerializer(fgs_results, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        print(request.data)
        new_fgs = {
            'fungal_gene':request.data.get('fungal_gene'),

            'pcr_results':request.data.get('pcr_results'),
            'replicate_id':request.data.get('replicate_id'),
            'sample_id':request.data.get('sample_id'),
            'reference':request.data.get('reference'),
        }

        serializer = FGSSerializer(data=new_fgs)
        rice_genotype = None

        if request.data.get('rice_genotype') is not None:
            rice_genotype = RiceGenotype.objects.get(pk=request.data.get('rice_genotype'))   

        if serializer.is_valid():
            fgs = serializer.save()
            fgs.rice_genotype = rice_genotype 
            fgs.save()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  


    def put(self,request,format=None):
        print(request.data)
        fgs = FungalGeneScreenResult.objects.get(pk=request.data.get('pk'))

        if( isinstance(request.data.get('rice_genotype'),str)):
            rice_genotype = RiceGenotype.objects.get(name=request.data.get('rice_genotype'))
        else:
            rice_genotype = RiceGenotype.objects.get(pk=request.data.get('rice_genotype'))

        if fgs.pcr_results is not request.data.get('pcr_results'):
            fgs.pcr_results = request.data.get('pcr_results')
        if fgs.replicate_id is not request.data.get('replicate_id'):
            fgs.replicate_id = request.data.get('replicate_id')
        if fgs.sample_id is not request.data.get('sample_id'):
            fgs.sample_id = request.data.get('sample_id')
        if fgs.fungal_gene is not request.data.get('fungal_gene'):
            fgs.fungal_gene = request.data.get('fungal_gene')
        if fgs.rice_genotype.pk is not request.data.get('rice_genotype'): 
            fgs.rice_genotype = rice_genotype

        fgs.save()    
        return Response(status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        fgs = FungalGeneScreenResult.objects.get(pk=pk)
        fgs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PathotypingResultsList(APIView):
    '''
    All Pathotyping Results.
    '''
    def get(self,request,format=None):
        results = PathotypingResults.objects.all()
        serializer = PathotypingResultsSerializer(results, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        print(request.data)

        addData = {
            'sample_id':request.data.get('sample_id'),

            'replicate_id':request.data.get('replicate_id'),
            'stock_id':request.data.get('stock_id'),
            'date_inoculated':request.data.get('date_inoculated'),
            'date_scored':request.data.get('date_scored'),
            'date_planted':request.data.get('date_planted'),
            'disease_score':request.data.get('disease_score'),
            'test':request.data.get('test'),
            'tray':request.data.get('tray'),          
        }

        serializer = PathotypingResultsSerializer(data=addData)
        
        rice_genotype = None
        isolate = None
        person = None
        lab = None
        project = None        

        if request.data.get('rice_genotype') is not None:
            rice_genotype = RiceGenotype.objects.get(pk=request.data.get('rice_genotype'))   
        if request.data.get('isolate') is not None:
            isolate = Isolate.objects.get(pk=request.data.get('isolate'))  
        if request.data.get('person') is not None:
            person = People.objects.get(pk=request.data.get('person'))  
        if request.data.get('lab') is not None:
            lab = RiceBlastLab.objects.get(pk=request.data.ge/t('lab'))  
        if request.data.get('project') is not None:
            project = Project.objects.get(pk=request.data.get('project'))  


        if serializer.is_valid():
            data = serializer.save()

            data.isolate = isolate 
            data.person = person 
            data.lab = lab 
            data.project = project 
            data.rice_genotype = rice_genotype

            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

    def put(self,request,format=None):
        print(request.data)
        data = PathotypingResults.objects.get(pk=request.data.get('pk'))
        rice_genotype = None
        isolate = None
        person = None
        lab = None
        if( isinstance(request.data.get('rice_genotype'),int)):
            rice_genotype = RiceGenotype.objects.get(pk=request.data.get('rice_genotype'))
            print(rice_genotype)

        if( isinstance(request.data.get('isolate'),int)):
            isolate = Isolate.objects.get(pk=request.data.get('isolate'))
            print(isolate)


        if( isinstance(request.data.get('person'),int)):
            person = People.objects.get(pk=request.data.get('person'))
            print(person)


        if( isinstance(request.data.get('lab'),int)):
            lab = RiceBlastLab.objects.get(pk=request.data.get('lab'))           
            print(lab)




        if data.stock_id is not request.data.get('stock_id'):
            data.stock_id = request.data.get('stock_id')
        if data.replicate_id is not request.data.get('replicate_id'):
            data.replicate_id = request.data.get('replicate_id')
        if data.sample_id is not request.data.get('sample_id'):
            data.sample_id = request.data.get('sample_id')
        if data.date_inoculated is not request.data.get('date_inoculated'):
            data.date_inoculated = request.data.get('date_inoculated')
        if data.date_planted is not request.data.get('date_planted'):
            data.date_planted = request.data.get('date_planted')
        if data.date_scored is not request.data.get('date_scored'):
            data.date_scored = request.data.get('date_scored')
        if data.disease_score is not request.data.get('disease_score'):
            data.disease_score = request.data.get('disease_score')                        
        if data.test is not request.data.get('test'):
            data.test = request.data.get('test')  
        if data.tray is not request.data.get('tray'):
            data.tray = request.data.get('tray')              



        if data.isolate is not request.data.get('isolate') : 
            data.isolate = isolate
        if data.rice_genotype is not request.data.get('rice_genotype'): 
            data.rice_genotype = rice_genotype
        if data.person is not request.data.get('person'): 
            data.person = person
        if data.lab is not request.data.get('lab'): 
            data.lab = lab

                     
            
        data.save()    
        return Response(status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        data = PathotypingResults.objects.get(pk=pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VcgGroupList(APIView):
    '''
    All VCG Groups.
    '''
    def get(self,request,format=None):
        groups = VcgGroup.objects.all()
        serializer = VCGGroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):

        print(request.data)

        addData = {
            'group':request.data.get('group'),
            'vcg_id':request.data.get('vcg_id'),     
        }

        serializer = VCGGroupSerializer(data=addData)      
        person = None
        lab = None  

        if request.data.get('person') is not None:
            person = People.objects.get(pk=request.data.get('person'))  
        if request.data.get('lab') is not None:
            lab = RiceBlastLab.objects.get(pk=request.data.get('lab'))
        if serializer.is_valid():
            data = serializer.save()

            data.person = person 
            data.lab = lab 
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,format=None):
        print(request.data)
        data = VcgGroup.objects.get(pk=request.data.get('pk'))
        person = None
        lab = None
        if( isinstance(request.data.get('person'),int)):
            person = People.objects.get(pk=request.data.get('person'))
            print(person)


        if( isinstance(request.data.get('lab'),int)):
            lab = RiceBlastLab.objects.get(pk=request.data.get('lab'))           
            print(lab)


        if( isinstance(request.data.get('person'),int)):
            person = People.objects.get(pk=request.data.get('person'))
            print(person)


        if( isinstance(request.data.get('lab'),int)):
            lab = RiceBlastLab.objects.get(pk=request.data.get('lab'))           
            print(lab)




        if data.group is not request.data.get('group'):
            data.group = request.data.get('group')
        if data.vcg_id is not request.data.get('vcg_id'):
            data.vcg_id = request.data.get('vcg_id')

        if data.person is not request.data.get('person'): 
            data.person = person
        if data.lab is not request.data.get('lab'): 
            data.lab = lab
        data.save()    
        return Response(status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        data = VcgGroup.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT)     


class RiceSmallList(APIView):
    '''
    All Rice Small DNA Fragments.
    '''
    
    def get(self,request,format=None):
        rice_small = RiceSmallDnaFragmentsSequence.objects.all()
        serializer = RiceSmallSerializer(rice_small, many=True)
        return Response(serializer.data)


    def post(self,request,pk,format=None): 
        request_data = request.data.get('info')
        info = json.loads(request_data)
        print(info)
        file_upload = request.FILES.get('sequence_data')
        addData = {
            'taxa_name':info['taxa_name'],
            'sequence_id':info['sequence_id'],
            'description':info['description'],
            'sequence_data':file_upload,
            'chromosome_id':info['chromosome_id'],
            'chromosome_site_id':info['chromosome_site_id'],
            'loci_id':info['loci_id'],
            'target_gene':info['target_gene'],
        }   
            
        serializer = RiceSmallSerializer(data=addData)
        person = None
        rice_genotype = None
        lab = None
 
        if info['person'] != None and info['person'] != '':
            person = People.objects.get(pk=info['person']) 
 
        if info['rice_genotype'] != None and info['rice_genotype'] != '':
            rice_genotype = RiceGenotype.objects.get(pk=info['rice_genotype']) 
             
        if info['lab'] != None and info['lab'] != '':
            lab = RiceBlastLab.objects.get(pk=info['lab']) 

        if serializer.is_valid():
            data = serializer.save()

            data.person = person 
            data.rice_genotype = rice_genotype 

            data.lab = lab 

            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(serializer.errors)
 
        return Response(status=status.HTTP_400_BAD_REQUEST) 
        print(file_upload)        
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    def put(self,request,pk,format=None):    
        print(request.data)   
        return Response(status=status.HTTP_204_NO_CONTENT)                   
    def delete(self,request,pk,format=None):
        data = RiceSmallDnaFragmentsSequence.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT)   




class FungalSmallList(APIView):
    '''
    All Fungal Small DNA Fragments.
    '''
    def get(self,request,format=None):
        fungal_small = FungalSmallDnaFragmentsSequence.objects.all()
        serializer = FungalSmallSerializer(fungal_small, many=True)
        return Response(serializer.data)

    def post(self,request,pk,format=None):    
        # print(request.FILES)
        # print(request.data.get('info'))

        request_data = request.data.get('info')
        info = json.loads(request_data)
        file_upload = request.FILES.get('fungal_gene_sequence')
        print(file_upload)
        addData = {
            'activity_name':info['activity_name'],

            'fungal_gene_name':info['fungal_gene_name'],
            'fungal':info['fungal'],
            'fungal_gene_sequence':file_upload,
            'date_of_sequence':info['date_of_sequence'],
            'project_name':info['project_name'],
            'loci_id':info['loci_id'],
            'target_gene':info['target_gene'],
        }   

        serializer = FungalSmallSerializer(data=addData)
        person = None
# 
        if info['person'] != None and info['person'] != '':
            person = People.objects.get(pk=info['person']) 

        if serializer.is_valid():
            data = serializer.save()

            data.person = person 
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(serializer.errors)
 
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    def put(self,request,pk,format=None):    
        return Response(status=status.HTTP_204_NO_CONTENT)                   
    def delete(self,request,pk,format=None):
        data = FungalSmallDnaFragmentsSequence.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT)   


class VCGTestResultsList(APIView):
    '''
    All VCG TEST RESULTS LIST.
    '''
    def get(self,request,format=None):
        results = VCGTestResults.objects.all()
        serializer = VCGTestResultsSerializer(results, many=True)
        return Response(serializer.data)

    def post(self,request,pk,format=None):   
        print(request.data)
        addData = {
            'vcg_test_id':request.data.get('vcg_test_id'),

            'vcg_tester_id':request.data.get('vcg_tester_id'),
            'tester_complimented_isolate':request.data.get('tester_complimented_isolate'),
            'tester_and_control':request.data.get('tester_and_control'),
            'vcg_replicate_id':request.data.get('vcg_replicate_id'),
        }
        serializer = VCGTestResultsSerializer(data=addData)
        
        isolate = None
        lab = None
        vcg = None        

        if request.data.get('isolate') is not None:
            isolate = Isolate.objects.get(pk=request.data.get('isolate'))  
        if request.data.get('lab') is not None:
            lab = RiceBlastLab.objects.get(pk=request.data.get('lab'))  
        if request.data.get('vcg') is not None:
            vcg = VcgGroup.objects.get(pk=request.data.get('vcg'))  


        if serializer.is_valid():
            data = serializer.save()

            data.isolate = isolate 
            data.lab = lab 
            data.vcg = vcg 

            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):   
        print(request.data)
        data = VCGTestResults.objects.get(pk=request.data.get('pk'))
        isolate = None
        vcg = None
        lab = None
        if( isinstance(request.data.get('vcg'),int)):
            vcg = VcgGroup.objects.get(pk=request.data.get('vcg'))
            print(vcg)

        if( isinstance(request.data.get('isolate'),int)):
            isolate = Isolate.objects.get(pk=request.data.get('isolate'))
            print(isolate)


        if( isinstance(request.data.get('lab'),int)):
            lab = RiceBlastLab.objects.get(pk=request.data.get('lab'))           
            print(lab)




        if data.vcg_test_id is not request.data.get('vcg_test_id'):
            data.vcg_test_id = request.data.get('vcg_test_id')
        if data.vcg_tester_id is not request.data.get('vcg_tester_id'):
            data.vcg_tester_id = request.data.get('vcg_tester_id')
        if data.tester_complimented_isolate is not request.data.get('tester_complimented_isolate'):
            data.tester_complimented_isolate = request.data.get('tester_complimented_isolate')
        if data.tester_and_control is not request.data.get('tester_and_control'):
            data.tester_and_control = request.data.get('tester_and_control')
        if data.vcg_replicate_id is not request.data.get('vcg_replicate_id'):
            data.vcg_replicate_id = request.data.get('vcg_replicate_id')        

        if data.isolate is not request.data.get('isolate'): 
            data.isolate = isolate
        if data.vcg is not request.data.get('vcg'): 
            data.vcg = vcg
        if data.lab is not request.data.get('lab'): 
            data.lab = lab     
        data.save()    
        return Response(status=status.HTTP_200_OK)
        
    def delete(self,request,pk,format=None):
        data = VCGTestResults.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT)   




class ProtocolList(APIView):
    '''
    All Protocols.
    '''
    def get(self,request,format=None):
        results = Protocol.objects.all()
        serializer = ProtocolSerializer(results, many=True)
        return Response(serializer.data)

    def post(self,request,pk,format=None):    

        request_data = request.data.get('info')
        info = json.loads(request_data)
        file_upload = request.FILES.get('protocol')
        print(file_upload)
        addData = {

            'name':info['name'],
            'protocol':file_upload,

        }   

        serializer = ProtocolSerializer(data=addData)

        if serializer.is_valid():
            data = serializer.save()
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(serializer.errors)
 
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    def put(self,request,pk,format=None):    
        return Response(status=status.HTTP_204_NO_CONTENT)                   
    def delete(self,request,pk,format=None):
        data = Protocol.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT) 

class RiceGBSList(APIView):
    '''
    All Rice GBS.
    '''

    def get(self,request,format=None):
        results = RiceGBS.objects.all()
        serializer = RiceGBSSerializer(results, many=True)
        return Response(serializer.data)
    def post(self,request,pk,format=None):
        request_data = request.data.get('info')
        info = json.loads(request_data)
        file_upload = request.FILES.get('gbs_dataset')
        print(file_upload)
        addData = {

            'rice_gbs_name':info['rice_gbs_name'],
            'gbs_dataset':file_upload,

        }   

        serializer = RiceGBSSerializer(data=addData)
        person = None
        lab = None
        if info['person'] != None and info['person'] != '':
            person = People.objects.get(pk=info['person']) 
          
        if info['lab'] != None and info['lab'] != '':
            lab = RiceBlastLab.objects.get(pk=info['lab'])        

        if serializer.is_valid():
            data = serializer.save()
            data.person = person
            data.lab = lab
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(serializer.errors)
 
        return Response(status=status.HTTP_400_BAD_REQUEST)     
    def put(self,request,pk,format=None):    
        return Response(status=status.HTTP_204_NO_CONTENT)                   
    def delete(self,request,pk,format=None):
        data = RiceGBS.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT) 

class FungalGBSList(APIView):
    '''
    All Fungal GBS.
    '''
    def get(self,request,format=None):
        results = FungalGBS.objects.all()
        serializer = FungalGBSSerializer(results, many=True)
        return Response(serializer.data)    
    def post(self,request,pk,format=None):    
        request_data = request.data.get('info')
        info = json.loads(request_data)
        file_upload = request.FILES.get('gbs_dataset')
        print(file_upload)
        addData = {

            'fungal_gbs_name':info['fungal_gbs_name'],
            'gbs_dataset':file_upload,

        }   

        serializer = FungalGBSSerializer(data=addData)
        person = None
        lab = None
        if info['person'] != None and info['person'] != '':
            person = People.objects.get(pk=info['person']) 
          
        if info['lab'] != None and info['lab'] != '':
            lab = RiceBlastLab.objects.get(pk=info['lab'])        

        if serializer.is_valid():
            data = serializer.save()
            data.person = person
            data.lab = lab
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(serializer.errors)
 
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    def put(self,request,pk,format=None):    
        return Response(status=status.HTTP_204_NO_CONTENT)                   
    def delete(self,request,pk,format=None):
        data = FungalGBS.objects.get(pk=pk)
        data.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT) 

@api_view(['GET'])
def download_file(request):

    '''
    Download File
    '''
    # file_name=request.GET.get('name')
    # print(request.GET.get('name'))
# 
    # the_f = FungalSmallDnaFragmentsSequence.objects.get(pk=1)
    # print(the_f.fungal_gene_sequence)

    print(request.GET.get('name'))
    file_name=request.GET.get('name')
    file_path = settings.BASE_DIR  + file_name
    with open(file_path,'rb') as download:
        # red = download.read()
        response = HttpResponse(FileWrapper(download))
        response['Content-Disposition'] = 'attachment; filename=NameOfFile'
        return response
# 
        # return Response({'data':fd})
    return Response(status=status.HTTP_400_BAD_REQUEST)