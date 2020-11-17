# Generated by Django 3.0.3 on 2020-11-17 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vcgtestresults',
            name='isolate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.Isolate'),
        ),
        migrations.AlterField(
            model_name='vcgtestresults',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.RiceBlastLab'),
        ),
        migrations.AlterField(
            model_name='vcgtestresults',
            name='vcg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riceapp.VcgGroup'),
        ),
    ]
