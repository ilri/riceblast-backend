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



class Field(models.Model):
    '''Model class for Collection Fields '''

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='field_person')
    country = CountryField()
    latitude = models.DecimalField(default=0.0000,max_digits=6, decimal_places=4)
    longitude = models.DecimalField(default=0.0000,max_digits=6, decimal_places=4)
    
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
    field = models.ForeignKey(Field,on_delete=models.CASCADE)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    tissue_type = models.CharField(max_length=100)

    def __str__(self):
        return self.isolate_id


class RiceGenotype(models.Model):
    name = models.CharField(max_length=200)
    rice_genotype_id = models.CharField(max_length=100, unique=True) 
    resistance_genes = models.CharField(max_length=200)
    r_gene_sources = models.CharField(max_length=200)
    susceptible_background = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PathotypingResults(models.Model):
    replicate_id = models.CharField(max_length=100,unique=True)
    sample_id = models.CharField(max_length=100, unique=True)
    rice_genotype = models.ForeignKey(RiceGenotype, on_delete=models.CASCADE)
    isolate = models.ForeignKey(Isolate, on_delete=models.CASCADE)
    stock_id = models.CharField(max_length=100, unique=True)
    date_inoculated = models.DateField()
    date_scored = models.DateField()
    date_planted = models.DateField()
    person = models.ForeignKey(People,on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    disease_score = models.IntegerField()
    test_id = models.CharField(unique=True,max_length=100)

    def __str__(self):
        return self.sample_id

class VcgGroup(models.Model):
    group = models.CharField(max_length=200)
    vcg_id = models.CharField(max_length=100, unique=True) 
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    person = models.ForeignKey(People, on_delete=models.CASCADE)

    def __str__(self):
        return self.group 

class DNASequence(models.Model):
    isolate = models.ForeignKey(Isolate, on_delete=models.CASCADE)
    taxa_name = models.CharField(max_length=200)
    sequence_id = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    sequence_data = models.CharField(max_length=200)
    chromosome_id = models.CharField(max_length=100,unique=True)
    chromosome_site_id = models.CharField(max_length=100,unique=True)
    loci_id = models.CharField(max_length=100,unique=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)

    def __str__(self):
        return self.sequence_id 

class VCGTest(models.Model):
    vcg_test_id = models.CharField(max_length=100, unique=True)
    isolate = models.ForeignKey(Isolate,on_delete=models.CASCADE)
    vcg_tester_id = models.CharField(max_length=100, unique=True)
    tester_complimented_isolate = models.BooleanField()
    # tester + control
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    vcg_replicate_id = models.CharField(max_length=100,unique=True)
    vcg = models.ForeignKey(VcgGroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vcg_test_id 

class Protocol(models.Model):
    name = models.CharField(max_length=200)
    protocol_id = models.CharField(max_length=100, unique=True)
    key_reference = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    protocol_modified = models.BooleanField()
    related_protocols = models.CharField(max_length=200)
    country = CountryField(multiple=True)

    def __str__(self):
        return self.protocol_id


class RiceGBS(models.Model):
    rice_gbs_name = models.CharField(max_length=200)
    person = models.ForeignKey(People,on_delete=models.CASCADE)
    lab = models.ForeignKey(RiceBlastLab, on_delete=models.CASCADE)
    gbs_list = models.CharField(max_length=200)
    gbs_dataset = models.CharField(max_length=200)

    def __str__(self):
        return self.rice_gbs_name

