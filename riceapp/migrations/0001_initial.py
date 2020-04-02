# Generated by Django 3.0.3 on 2020-03-23 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Isolate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isolate_id', models.CharField(max_length=100)),
                ('isolate_name', models.CharField(max_length=200)),
                ('taxa_name', models.CharField(blank=True, max_length=200)),
                ('tissue_type', models.CharField(max_length=100, null=True)),
                ('date_collected', models.CharField(blank=True, max_length=100)),
                ('date_isolated', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('host_genotype', models.CharField(blank=True, max_length=255)),
                ('collection_site', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(max_length=100)),
                ('telephone_number', models.IntegerField()),
                ('designation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('donor', models.CharField(max_length=255)),
                ('start', models.DateField()),
                ('finish', models.DateField()),
                ('prinicipal_investigator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
            ],
        ),
        migrations.CreateModel(
            name='RiceBlastLab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_id', models.CharField(max_length=100, unique=True)),
                ('lab_name', models.CharField(max_length=200)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('institution', models.CharField(max_length=200)),
                ('principal_investigator', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RiceGene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('chromosome_id', models.IntegerField(blank=True, null=True)),
                ('marker', models.CharField(blank=True, max_length=100, null=True)),
                ('donor_line', models.CharField(blank=True, max_length=255, null=True)),
                ('resistance_type', models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Partial', 'Partial')], max_length=50, null=True)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RiceGenotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rice_genotype_id', models.CharField(blank=True, max_length=100, null=True)),
                ('resistance_genes', models.CharField(blank=True, max_length=200, null=True)),
                ('r_gene_sources', models.CharField(blank=True, max_length=200, null=True)),
                ('susceptible_background', models.CharField(blank=True, max_length=200, null=True)),
                ('accession_number', models.CharField(blank=True, max_length=100, null=True)),
                ('pedigree', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, choices=[('released_variety', 'Released Variety'), ('microgenic_line', 'Microgenic Line'), ('interspecific_variety', 'Interspecific Variety'), ('introgession_line', 'Introgession Line'), ('adapted_african_cultiva', 'Adapted African Cultiva')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VcgGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, max_length=200, null=True)),
                ('vcg_id', models.CharField(blank=True, max_length=100, null=True)),
                ('lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
            ],
        ),
        migrations.CreateModel(
            name='VCGTestResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vcg_test_id', models.CharField(max_length=100, unique=True)),
                ('vcg_tester_id', models.CharField(max_length=100)),
                ('tester_complimented_isolate', models.BooleanField()),
                ('tester_and_control', models.BooleanField()),
                ('vcg_replicate_id', models.CharField(max_length=100)),
                ('isolate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.Isolate')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.Project')),
                ('vcg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.VcgGroup')),
            ],
        ),
        migrations.CreateModel(
            name='RiceSmallDnaFragmentsSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxa_name', models.CharField(max_length=200)),
                ('sequence_id', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('sequence_data', models.FileField(upload_to='rice_sequence_data/')),
                ('chromosome_id', models.IntegerField()),
                ('chromosome_site_id', models.CharField(max_length=100)),
                ('loci_id', models.CharField(max_length=100)),
                ('target_gene', models.CharField(max_length=255)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
                ('rice_genotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceGenotype')),
            ],
        ),
        migrations.CreateModel(
            name='RiceGeneScreenResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcr_results', models.CharField(max_length=100)),
                ('replicate_id', models.CharField(max_length=20)),
                ('sample_id', models.CharField(max_length=100)),
                ('rice_gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceGene')),
                ('rice_genotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceGenotype')),
            ],
        ),
        migrations.CreateModel(
            name='RiceGBS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rice_gbs_name', models.CharField(max_length=200)),
                ('gbs_dataset', models.FileField(upload_to='rice_gbs_dataset/')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
            ],
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('protocol_id', models.CharField(max_length=100, unique=True)),
                ('key_reference', models.CharField(max_length=500)),
                ('protocol', models.FileField(upload_to='protocols/')),
                ('protocol_modified', models.DateField()),
                ('related_protocols', models.CharField(max_length=200)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
            ],
        ),
        migrations.AddField(
            model_name='people',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_people', to='riceapp.RiceBlastLab'),
        ),
        migrations.CreateModel(
            name='PathotypingResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replicate_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sample_id', models.CharField(blank=True, max_length=100, null=True)),
                ('stock_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date_inoculated', models.DateField(blank=True, null=True)),
                ('date_scored', models.DateField(blank=True, null=True)),
                ('date_planted', models.DateField(blank=True, null=True)),
                ('disease_score', models.IntegerField(blank=True, null=True)),
                ('test', models.CharField(blank=True, max_length=100, null=True)),
                ('tray', models.CharField(blank=True, max_length=100, null=True)),
                ('isolate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.Isolate')),
                ('lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.Project')),
                ('rice_genotype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceGenotype')),
            ],
        ),
        migrations.AddField(
            model_name='isolate',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.People'),
        ),
        migrations.CreateModel(
            name='FungalSmallDnaFragmentsSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxa_name', models.CharField(max_length=200)),
                ('sequence_id', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('sequence_data', models.FileField(upload_to='fungal_sequence_data/')),
                ('chromosome_id', models.IntegerField()),
                ('chromosome_site_id', models.CharField(max_length=100)),
                ('loci_id', models.CharField(max_length=100)),
                ('target_gene', models.CharField(max_length=255)),
                ('isolate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.Isolate')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
            ],
        ),
        migrations.CreateModel(
            name='FungalGeneScreenResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fungal_gene', models.CharField(max_length=255)),
                ('pcr_results', models.CharField(max_length=100)),
                ('replicate_id', models.CharField(max_length=20)),
                ('sample_id', models.CharField(max_length=100)),
                ('rice_genotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceGenotype')),
            ],
        ),
        migrations.CreateModel(
            name='FungalGBS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fungal_gbs_name', models.CharField(max_length=200)),
                ('gbs_dataset', models.FileField(upload_to='fungal_gbs_dataset')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riceapp.People')),
            ],
        ),
        migrations.CreateModel(
            name='FungalCollectionSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('longitude', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_person', to='riceapp.People')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.Project')),
            ],
        ),
    ]
