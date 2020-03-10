from .models import *
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .forms import RiceGeneConfirmImportForm,RiceGeneImportForm

class FungalCollectionSiteResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request',None)
        super(FungalCollectionSiteResource, self).__init__(*args, **kwargs)
    
    def before_import(self,dataset, using_transactions, dry_run, **kwargs):
        for i,header in enumerate(dataset.headers):
            print(dataset)
            dataset.headers[i] = header.lower()
    
    def before_import_row(self,row,**kwargs):
        country = self.request.POST.get('country')
        project = self.request.POST.get('project')
        person = self.request.POST.get('person')
        row['country'] = country
        row['project'] = project
        row['person'] = person

    class Meta:
        model = FungalCollectionSite

class IsolateResource(resources.ModelResource):
    class Meta:
        model = Isolate
    
    def before_import(self,dataset, using_transactions, dry_run, **kwargs):
        for i,header in enumerate(dataset.headers):
            dataset.headers[i] = header.lower()

class VcgTestResultsResource(resources.ModelResource):
    class Meta:
        model = VCGTestResults

class FungalSmallDnaFragmentsSequenceResource(resources.ModelResource):
    class Meta:
        model = FungalSmallDnaFragmentsSequence

class RiceSmallDnaFragmentsSequenceResource(resources.ModelResource):
    class Meta:
        model = RiceSmallDnaFragmentsSequence

class RiceGenotypeResource(resources.ModelResource):
    class Meta:
        model = RiceGenotype
    
    def before_import(self,dataset, using_transactions, dry_run, **kwargs):
        for i,header in enumerate(dataset.headers):
            dataset.headers[i] = header.lower()
    def before_import_row(self,row, **kwargs):
        row['name'] = str(row['name'])

class PathotypingResultsResource(resources.ModelResource):
    class Meta:
        model = PathotypingResults
    
    def before_import(self,dataset, using_transactions, dry_run, **kwargs):
        for i,header in enumerate(dataset.headers):
            dataset.headers[i] = header.lower()
    def before_import_row(self,row,**kwargs):
        try:
            isolate = Isolate.objects.get(isolate_id=row['isolate'])          
            row['isolate'] = isolate.pk
        except Isolate.DoesNotExist:
            row['isolate'] = None
        
        try:
            RiceGenotype.objects.get(pk=row['rice_genotype'])
        except RiceGenotype.DoesNotExist:
            row['rice_genotype'] = None

        


class RiceGeneResource(resources.ModelResource):

    class Meta:
        model = RiceGene

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request',None)
        super(RiceGeneResource, self).__init__(*args, **kwargs)
    
    def before_import(self,dataset, using_transactions, dry_run, **kwargs):
        for i,header in enumerate(dataset.headers):
            dataset.headers[i] = header.lower()
    
    # def before_import_row(self,row,**kwargs):
        # donor_line = self.request.POST.get('donor_line')
        # row['donor_line'] = donor_line 
