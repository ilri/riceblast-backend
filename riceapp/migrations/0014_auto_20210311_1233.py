# Generated by Django 3.0.3 on 2021-03-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riceapp', '0013_auto_20210303_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ricegene',
            old_name='marker',
            new_name='marker_type',
        ),
        migrations.AddField(
            model_name='ricegene',
            name='marker_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
