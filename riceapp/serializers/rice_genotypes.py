from rest_framework import serializers
from ..models import RiceGenotype

class RiceGenotypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = RiceGenotype
        fields = ('name','rice_genotype_id','resistance_genes','r_gene_sources',
                'susceptible_background','accession_number','pedigree','category' )