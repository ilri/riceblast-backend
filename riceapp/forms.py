from django import forms
from import_export.forms import ImportForm, ConfirmImportForm
from .models import *
from django_countries.data import COUNTRIES

class FungalCollectionSiteImportForm(ImportForm):
    country = forms.ChoiceField(choices=COUNTRIES.items())

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
    )

    person = forms.ModelChoiceField(
        queryset=People.objects.all(),
        required=True
    )
class FungalCollectionSiteConfirmForm(ConfirmImportForm):
    country = forms.ChoiceField(choices=COUNTRIES.items())

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
    )

    person = forms.ModelChoiceField(
        queryset=People.objects.all(),
        required=True
    )

class IsolateImportForm(ImportForm):
    # country = forms.ChoiceField(choices=COUNTRIES.items())
    # collection_site = forms.ModelChoiceField(
        # queryset=FungalCollectionSite.objects.all(),
        # required=True,
    # )
    person = forms.ModelChoiceField(
        queryset=People.objects.all(),
        required=False
    )


class IsolateConfirmForm(ConfirmImportForm):
    # collection_site = forms.ModelChoiceField(
        # queryset=FungalCollectionSite.objects.all(),
        # required=True,
    # )
    person = forms.ModelChoiceField(
        queryset=People.objects.all(),
        required=False
    )

class VcgTestResultsImportForm(ImportForm):
    pass
class VcgTestResultsConfirmForm(ConfirmImportForm):
    pass

class FungalSmallDnaFragmentsSequenceImportForm(ImportForm):
    pass
class FungalSmallDnaFragmentsSequenceConfirmImportForm(ConfirmImportForm):
    pass

class RiceSmallDnaFragmentsSequenceImportForm(ImportForm):
    pass
class RiceSmallDnaFragmentsSequenceConfirmImportForm(ConfirmImportForm):
    pass

class RiceGenotypeImportForm(ImportForm):
    pass
class RiceGenotypeConfirmImportForm(ConfirmImportForm):
    pass

class PathotypingResultsImportForm(ImportForm):
    lab = forms.ModelChoiceField(
        queryset=RiceBlastLab.objects.all(),
        required=False,
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
    )
    person = forms.ModelChoiceField(
        queryset=People.objects.all(),
        required=False,
    )


class PathotypingResultsConfirmImportForm(ConfirmImportForm):
    lab = forms.ModelChoiceField(
        queryset=RiceBlastLab.objects.all(),
        required=False,

    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
    )
    person = forms.ModelChoiceField(
        queryset=People.objects.all(),
        required=False,
    )

class RiceGeneImportForm(ImportForm):
    # donor_line = forms.ModelChoiceField(
        # queryset=RiceGenotype.objects.all(),
        # required=True
    # )
    pass
class RiceGeneConfirmImportForm(ConfirmImportForm):
    # donor_line = forms.ModelChoiceField(
        # queryset=RiceGenotype.objects.all(),
        # required=True
    # )
    pass