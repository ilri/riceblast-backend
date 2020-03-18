# Generated by Django 3.0.3 on 2020-03-18 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riceapp', '0002_pathotypingresults_tray'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fungalcollectionsite',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_person', to='riceapp.People'),
        ),
        migrations.AlterField(
            model_name='fungalcollectionsite',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.Project'),
        ),
        migrations.AlterField(
            model_name='people',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_people', to='riceapp.RiceBlastLab'),
        ),
        migrations.AlterField(
            model_name='project',
            name='prinicipal_investigator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.People'),
        ),
    ]
