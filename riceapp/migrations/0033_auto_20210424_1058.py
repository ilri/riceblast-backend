# Generated by Django 3.0.3 on 2021-04-24 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riceapp', '0032_auto_20210423_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('USER', 'USER')], default='USER', max_length=50),
        ),
    ]
