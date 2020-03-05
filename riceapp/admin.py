from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin,ImportMixin
from import_export.forms import ImportForm, ConfirmImportForm
from import_export.widgets import ForeignKeyWidget
from django import forms


# Register your models here.
class RiceGeneImportForm(ImportForm):
    donor_line = forms.ModelChoiceField(
        queryset=RiceGenotype.objects.all(),
        required=True
    )
class RiceGeneConfirmImportForm(ConfirmImportForm):
    donor_line = forms.ModelChoiceField(
        queryset=RiceGenotype.objects.all(),
        required=True
    )
class RiceGeneResource(resources.ModelResource):

    class Meta:
        model = RiceGene

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request',None)
        super(RiceGeneResource, self).__init__(*args, **kwargs)
    
    def before_import(self,dataset, using_transactions, dry_run, **kwargs):
        for i,header in enumerate(dataset.headers):
            dataset.headers[i] = header.lower()
    
    def before_import_row(self,row,**kwargs):
        donor_line = self.request.POST.get('donor_line')
        row['donor_line'] = donor_line 





class RiceGeneAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = RiceGeneResource

    def get_import_form(self):
        return RiceGeneImportForm
    def get_confirm_import_form(self):
        return RiceGeneConfirmImportForm
    
    def get_form_kwargs(self,form,*args, **kwargs):
        # pass on `donor_line` to the kwargs for the custom confirm form
        # print(isinstance(form, ImportForm))
        # print(form)
        if isinstance(form, RiceGeneImportForm):
            print(form.is_valid())
            if form.is_valid():
                donor_line = form.cleaned_data['donor_line']
                kwargs.update({'donor_line':donor_line})
        return kwargs

    def get_resource_kwargs(self,request,*args, **kwargs):
        return {'request':request}
    

admin.site.site_header = 'Rice Blast'

admin.site.register(RiceBlastLab)
admin.site.register(People)
admin.site.register(FungalCollectionSite)
admin.site.register(Isolate)
admin.site.register(RiceGenotype)
admin.site.register(PathotypingResults)
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




