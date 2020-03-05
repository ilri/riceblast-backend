from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField



# Create your models here.
class RiceBlastLab(models.Model):
    ''' Model class for Rice Blast Labs '''
    lab_id = models.CharField(max_length=100, unique=True)
    lab_name = models.CharField(max_length=200)
    country = CountryField()
    institution = models.CharField(max_length=200)
    principal_investigator = models.CharField(max_length=100)

    def __str__(self):
        return self.lab_name
        
class People(models.Model):
    ''' Model class for Lab People '''

    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    telephone_number = models.IntegerField()
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE, related_name='lab_people')
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    donor = models.CharField(max_length=255)
    start = models.DateField()
    finish = models.DateField()
    prinicipal_investigator = models.ForeignKey(People, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name

class FungalCollectionSite(models.Model):
    ''' Model class for Collection Fields '''

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='field_person')
    country = CountryField()
    latitude = models.DecimalField(default=0.0000,max_digits=6, decimal_places=4)
    longitude = models.DecimalField(default=0.0000,max_digits=6, decimal_places=4)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Isolate(models.Model):
    '''Model class for lab isolates'''
    isolate_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    taxa_name = models.CharField(max_length=200)
    date_collected = models.DateField() #!!!
    date_isolated = models.DateField() #!!!!
    country = CountryField()
    collection_site = models.ForeignKey(FungalCollectionSite,on_delete=models.CASCADE)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    tissue_type = models.CharField(max_length=100)

    def __str__(self):
        return self.isolate_id



    
class RiceGenotype(models.Model):
    CATEGORY_CHOICES = [
        ('released_variety','Released Variety'),
        ('microgenic_line','Microgenic Line'),
        ('interspecific_variety','Interspecific Variety'),
        ('introgession_line', 'Introgession Line'),
        ('adapted_african_cultiva', 'Adapted African Cultiva')
    ]
    name = models.CharField(max_length=200)
    rice_genotype_id = models.CharField(max_length=100, unique=True) 
    resistance_genes = models.CharField(max_length=200)
    r_gene_sources = models.CharField(max_length=200)
    susceptible_background = models.CharField(max_length=200)
    accession_number = models.CharField(max_length=100)
    pedigree = models.CharField(max_length=100)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class RiceGene(models.Model):
    name = models.CharField(max_length=100)
    chromosome_id = models.IntegerField()
    marker = models.CharField(max_length=100)
    donor_line = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class RiceGeneScreenResult(models.Model):
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE)
    rice_gene = models.ForeignKey(RiceGene, on_delete=models.CASCADE)
    pcr_results = models.CharField(max_length=100) #POSITIVE OR NEGATIVE
    replicate_id = models.CharField(max_length=20) #1,2,3
    sample_id = models.CharField(max_length=100)

    def __str__(self):
        return self.sample_id

class FungalGeneScreenResult(models.Model):
    fungal_gene = models.CharField(max_length=255)
    rice_genotype = models.ForeignKey(RiceGenotype,on_delete=models.CASCADE) 
    pcr_results = models.CharField(max_length=100) #POSITIVE OR NEGATIVE
    replicate_id = models.CharField(max_length=20) #1,2,3
    sample_id = models.CharField(max_length=100)

    def __str__(self):
        return self.fungal_gene


class PathotypingResults(models.Model):
    replicate_id = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=100, unique=True)
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE)
    isolate = models.ForeignKey(Isolate, on_delete=models.CASCADE)
    stock_id = models.CharField(max_length=100)
    date_inoculated = models.DateField()
    date_scored = models.DateField()
    date_planted = models.DateField()
    person = models.ForeignKey(People,on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    disease_score = models.IntegerField()
    test_id = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.sample_id

class VcgGroup(models.Model):
    group = models.CharField(max_length=200)
    vcg_id = models.CharField(max_length=100, unique=True) 
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    person = models.ForeignKey(People, on_delete=models.CASCADE)

    def __str__(self):
        return self.group 

class FungalSmallDnaFragmentsSequence(models.Model):
    isolate = models.ForeignKey(Isolate, on_delete=models.CASCADE)
    taxa_name = models.CharField(max_length=200)
    sequence_id = models.CharField(max_length=100, unique=True) #unique or not?
    description = models.TextField()
    sequence_data = models.FileField(upload_to='fungal_sequence_data/') #UPLOAD A FASTA FILE
    chromosome_id = models.IntegerField()
    chromosome_site_id = models.CharField(max_length=100)
    loci_id = models.CharField(max_length=100)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    target_gene = models.CharField(max_length=255)

    def __str__(self):
        return self.sequence_id 

class RiceSmallDnaFragmentsSequence(models.Model):
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE)
    taxa_name = models.CharField(max_length=200)
    sequence_id = models.CharField(max_length=100, unique=True) #unique or not?
    description = models.TextField()
    sequence_data = models.FileField(upload_to='rice_sequence_data/') #UPLOAD A FASTA FILE
    chromosome_id = models.IntegerField()
    chromosome_site_id = models.CharField(max_length=100)
    loci_id = models.CharField(max_length=100)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    target_gene = models.CharField(max_length=255)

    def __str__(self):
        return self.sequence_id 

class VCGTestResults(models.Model):
    vcg_test_id = models.CharField(max_length=100, unique=True)
    isolate = models.ForeignKey(Isolate,on_delete=models.CASCADE)
    vcg_tester_id = models.CharField(max_length=100)
    tester_complimented_isolate = models.BooleanField()
    tester_and_control = models.BooleanField()
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    vcg_replicate_id = models.CharField(max_length=100)
    vcg = models.ForeignKey(VcgGroup, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vcg_test_id 

class Protocol(models.Model):
    name = models.CharField(max_length=200)
    protocol_id = models.CharField(max_length=100, unique=True)
    key_reference = models.CharField(max_length=500)
    protocol = models.FileField(upload_to='protocols/') #UPLOAD FILE
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    protocol_modified = models.DateField()
    related_protocols = models.CharField(max_length=200)
    # country = CountryField(multiple=True)

    def __str__(self):
        return self.protocol_id


class RiceGBS(models.Model):
    rice_gbs_name = models.CharField(max_length=200)
    person = models.ForeignKey(People,on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    gbs_dataset = models.FileField(upload_to='rice_gbs_dataset/') #UPLOAD VCF/HAPMAP FILE

    def __str__(self):
        return self.rice_gbs_name

class FungalGBS(models.Model):
    fungal_gbs_name = models.CharField(max_length=200)
    person = models.ForeignKey(People,on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    gbs_dataset = models.FileField(upload_to='fungal_gbs_dataset') #UPLOAD VCF/HAPMAP FILE

    def __str__(self):
        return self.fungal_gbs_name