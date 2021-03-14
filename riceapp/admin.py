from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin,ImportMixin,ImportExportMixin
from import_export.widgets import ForeignKeyWidget
from .forms import *
from .resources import * 


# Register your models here.

class FungalCollectionSiteAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = FungalCollectionSiteResource

    def get_import_form(self):
        return FungalCollectionSiteImportForm
    def get_confirm_import_form(self):
        return FungalCollectionSiteConfirmForm

    def get_form_kwargs(self,form,*args, **kwargs):
        # pass on `donor_line` to the kwargs for the custom confirm form
        if isinstance(form, FungalCollectionSiteImportForm):
            if form.is_valid():
                country = form.cleaned_data['country']
                person = form.cleaned_data['person']
                project = form.cleaned_data['project']
                
                kwargs.update({
                    'country':country,
                    'person':person,
                    'project':project,
                })
        return kwargs

    def get_resource_kwargs(self,request,*args, **kwargs):
        return {'request':request}    

#>>>>>>>>>Isolate Admin<<<<<<<<<<<<<<<<
class IsolateAdmin(ImportExportModelAdmin):
    resource_class = IsolateResource

    def get_import_form(self):
        return IsolateImportForm
    def get_confirm_import_form(self):
        return IsolateConfirmForm
    

class RiceGenotypeAdmin(ImportExportModelAdmin):
    resource_class = RiceGenotypeResource



class PathotypingResultsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = PathotypingResultsResource

    def get_import_form(self):
        return PathotypingResultsImportForm
    def get_confirm_import_form(self):
        return PathotypingResultsConfirmImportForm



class RiceGeneAdmin(ImportExportModelAdmin):
    resource_class = RiceGeneResource

    # def get_import_form(self):
        # return RiceGeneImportForm
    # def get_confirm_import_form(self):
        # return RiceGeneConfirmImportForm
    # 

    # def get_form_kwargs(self,form,*args, **kwargs):
        # pass on `donor_line` to the kwargs for the custom confirm form
        # if isinstance(form, RiceGeneImportForm):
            # if form.is_valid():
                # donor_line = form.cleaned_data['donor_line']
                # kwargs.update({'donor_line':donor_line})
        # return kwargs
# 
    # def get_resource_kwargs(self,request,*args, **kwargs):
        # return {'request':request}
    

admin.site.site_header = 'Rice Blast'

admin.site.register(RiceBlastLab)
admin.site.register(People)
admin.site.register(FungalCollectionSite, FungalCollectionSiteAdmin)
admin.site.register(Isolate, IsolateAdmin)
admin.site.register(RiceGenotype, RiceGenotypeAdmin)
admin.site.register(PathotypingResults, PathotypingResultsAdmin)
admin.site.register(VcgGroup)
admin.site.register(FungalSmallDnaFragmentsSequence)
admin.site.register(VCGTestResults)
admin.site.register(Protocol)
admin.site.register(RiceGBS)

admin.site.register(RiceGene, RiceGeneAdmin)
admin.site.register(RiceGeneScreenResult)
admin.site.register(RiceSmallDnaFragmentsSequence)
admin.site.register(FungalGBS)
admin.site.register(FungalGeneScreenResult)
admin.site.register(Project)
admin.site.register(Publications)
admin.site.register(Newsletters)
admin.site.register(Minutes)
admin.site.register(Outreach)





