from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# FUTURE MODFICATIONS 
# 1. Change use of in-built User model

    
# Create your models here.


class Publications(models.Model):
    '''Model class for Publications'''
    title=models.TextField()
    date=models.CharField(max_length=100)
    description=models.TextField()
    publication=models.FileField(upload_to='Publications/publication')

    class Meta:
        verbose_name_plural = 'Publications'

        
    def __str__(self):
        return self.title

class Newsletters(models.Model):
    '''Model class for Newsletters'''
    title=models.TextField()
    date=models.CharField(max_length=100)
    description=models.TextField()
    newsletter=models.FileField(upload_to='Newsletters/newsletter')

    class Meta:
        verbose_name_plural = 'Newsletters'

        
    def __str__(self):
        return self.title

class Minutes(models.Model):
    '''Model class for Minutes'''
    title=models.TextField()
    date=models.CharField(max_length=100)
    minutes=models.FileField(upload_to='Minutes/minutes')

    class Meta:
        verbose_name_plural = 'Minutes'

        
    def __str__(self):
        return self.title

class Outreach(models.Model):
    '''Model class for Outreach'''
    outreach=models.TextField()
    date=models.CharField(max_length=100)
    brief=models.TextField()
    image=models.ImageField(upload_to='Outreach/images', blank=True)
    outreach_file=models.FileField(upload_to='Outreach/outreach',blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Outreach'

        
    def __str__(self):
        return self.outreach

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
    ROLE_CHOICES = [
        ('ADMIN','ADMIN'),
        ('USER','USER'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=100)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE, related_name='lab_people',null=True,blank=True)
    designation = models.CharField(max_length=100)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,default='USER')

    class Meta:
        verbose_name_plural = 'People'

    def __str__(self):
        return self.full_name

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    donor = models.CharField(max_length=255)
    start = models.DateField()
    finish = models.DateField()
    prinicipal_investigator = models.ForeignKey(People, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.project_name

class FungalCollectionSite(models.Model):
    ''' Model class for Collection Fields '''

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(default=0.0000,max_digits=6, decimal_places=4)
    longitude = models.DecimalField(default=0.0000,max_digits=6, decimal_places=4)
    country = CountryField(default='KE')
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='field_person',null=True,blank=True)

    
    def __str__(self):
        return self.name

class Isolate(models.Model):
    '''Model class for lab isolates '''
    isolate_id = models.CharField(max_length=100)
    isolate_name = models.CharField(max_length=200,null=True,blank=True)
    # taxa_name = models.CharField(max_length=200,blank=True,null=True)
    tissue_type = models.CharField(max_length=100,null=True,blank=True)
    date_collected = models.CharField(max_length=100,blank=True,null=True)
    date_isolated = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    host_genotype = models.CharField(max_length=255,blank=True,null=True)
    collection_site = models.CharField(max_length=255,blank=True,null=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE,blank=True,null=True)

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
    name = models.CharField(max_length=255)
    rice_genotype_id = models.CharField(max_length=100,blank=True, null=True) #NOT UNIQUE 
    resistance_genes = models.CharField(max_length=200,blank=True, null=True)
    r_gene_sources = models.CharField(max_length=200,blank=True, null=True)
    susceptible_background = models.CharField(max_length=200,blank=True, null=True)
    accession_number = models.CharField(max_length=100,blank=True, null=True)
    pedigree = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,blank=True, null=True)
    project = models.CharField(max_length=200,null=True, blank=True) #CAN BE A FOREIGN KEY TO PROJECT TABLE

    def __str__(self):
        return self.name

class RiceGene(models.Model):

    RESISTANCE_CHOICES = [   

        ('Complete','Complete'),
        ('Partial','Partial'), 

    ]
    name = models.CharField(max_length=100,blank=True,null=True)
    chromosome_id = models.IntegerField(null=True,blank=True)
    marker_type = models.CharField(max_length=100,null=True,blank=True)
    marker_name = models.CharField(max_length=100,null=True,blank=True)
    donor_line = models.CharField(max_length=255,null=True,blank=True)
    # donor_line = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE, blank=True, null=True)
    resistance_type = models.CharField(choices=RESISTANCE_CHOICES, max_length=50,null=True,blank=True)
    reference = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

class RiceGeneScreenResult(models.Model):
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE,blank=True,null=True)
    rice_gene = models.ForeignKey(RiceGene, on_delete=models.CASCADE,blank=True,null=True)
    pcr_results = models.CharField(max_length=100) #POSITIVE OR NEGATIVE
    replicate_id = models.CharField(max_length=20) #1,2,3
    sample_id = models.CharField(max_length=100)

    def __str__(self):
        return self.sample_id

class FungalGeneScreenResult(models.Model):
    fungal_gene = models.CharField(max_length=255)
    isolate = models.ForeignKey(Isolate,on_delete=models.CASCADE,null=True,blank=True) 
    pcr_results = models.CharField(max_length=100) #POSITIVE OR NEGATIVE
    replicate_id = models.CharField(max_length=20) #1,2,3
    sample_id = models.CharField(max_length=100)

    def __str__(self):
        return self.fungal_gene

# UPLOAD
class PathotypingResults(models.Model):
    replicate_id = models.CharField(max_length=100,blank=True,null=True)
    sample_id = models.CharField(max_length=100,null=True,blank=True)
    stock_id = models.CharField(max_length=100,null=True,blank=True)
    date_inoculated = models.CharField(max_length=100,null=True,blank=True)
    date_scored = models.CharField(max_length=100,null=True,blank=True)
    date_planted = models.CharField(max_length=100,null=True,blank=True)
    disease_score = models.CharField(max_length=100,blank=True,null=True)
    test = models.CharField(max_length=100,blank=True,null=True)
    tray = models.CharField(max_length=100,blank=True,null=True)
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE,null=True,blank=True)
    isolate = models.ForeignKey(Isolate, on_delete=models.CASCADE,null=True,blank=True)
    person = models.ForeignKey(People,on_delete=models.CASCADE,null=True,blank=True)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Pathotyping Results'


class VcgGroup(models.Model):
    group = models.CharField(max_length=200,null=True,blank=True)
    vcg_id = models.CharField(max_length=100, null=True,blank=True) 
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE,null=True,blank=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.group 
# FILE
class FungalSmallDnaFragmentsSequence(models.Model):
    activity_name = models.CharField(max_length=200)
    fungal_gene_name = models.CharField(max_length=100) #unique or not?
    fungal = models.TextField()
    fungal_gene_sequence = models.FileField(upload_to='FungalSmallDnaFragmentsSequence/fungal_gene_sequence/') #UPLOAD A FASTA FILE
    date_of_sequence = models.CharField(max_length=200)
    project_name = models.CharField(max_length=100)
    loci_id = models.CharField(max_length=100)
    person = models.ForeignKey(People, on_delete=models.CASCADE,null=True,blank=True)
    target_gene = models.CharField(max_length=255)


    def __str__(self):
        return self.activity_name 
# FILE
class RiceSmallDnaFragmentsSequence(models.Model):
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE,null=True,blank=True)
    taxa_name = models.CharField(max_length=200)
    sequence_id = models.CharField(max_length=100, unique=True) #unique or not?
    description = models.TextField()
    sequence_data = models.FileField(upload_to='RiceSmallDnaFragmentsSequence/rice_sequence_data/') #UPLOAD A FASTA FILE
    chromosome_id = models.IntegerField()
    chromosome_site_id = models.CharField(max_length=100)
    loci_id = models.CharField(max_length=100)
    person = models.ForeignKey(People, on_delete=models.CASCADE,null=True,blank=True)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE,null=True,blank=True)
    target_gene = models.CharField(max_length=255)

    def __str__(self):
        return self.sequence_id 

class VCGTestResults(models.Model):
    vcg_test_id = models.CharField(max_length=100, unique=True)
    isolate = models.ForeignKey(Isolate,on_delete=models.CASCADE,null=True,blank=True)
    vcg_tester_id = models.CharField(max_length=100)
    tester_complimented_isolate = models.BooleanField()
    tester_and_control = models.BooleanField()
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE,null=True,blank=True)
    vcg_replicate_id = models.CharField(max_length=100)
    vcg = models.ForeignKey(VcgGroup, on_delete=models.CASCADE,null=True,blank=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vcg_test_id 



# FILE
class Protocol(models.Model):
    name = models.CharField(max_length=200)
    # protocol_id = models.CharField(max_length=100, unique=True)
    # key_reference = models.CharField(max_length=500)
    protocol = models.FileField(upload_to='Protocol/protocols/') #UPLOAD FILE
    # person = models.ForeignKey(People, on_delete=models.CASCADE)
    # lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    # protocol_modified = models.DateField()
    # related_protocols = models.CharField(max_length=200)
    # country = CountryField(multiple=True)

    def __str__(self):
        return self.name

# FILE
class RiceGBS(models.Model):
    rice_gbs_name = models.CharField(max_length=200)
    person = models.ForeignKey(People,on_delete=models.CASCADE,null=True,blank=True)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE,null=True,blank=True)
    gbs_dataset = models.FileField(upload_to='RiceGBS/rice_gbs_dataset/') #UPLOAD VCF/HAPMAP FILE

    def __str__(self):
        return self.rice_gbs_name


# FILE
class FungalGBS(models.Model):
    fungal_gbs_name = models.CharField(max_length=200)
    person = models.ForeignKey(People,on_delete=models.CASCADE,null=True,blank=True)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE,null=True,blank=True)
    gbs_dataset = models.FileField(upload_to='FungalGBS/fungal_gbs_dataset/') #UPLOAD VCF/HAPMAP FILE

    def __str__(self):
        return self.fungal_gbs_name

class TestFileUpload(models.Model):
    """
    Test
    """
    # file_test = models.FieldFile(upload_to='test/')      
    name = models.CharField(max_length=50, blank=True, null=True)  