# Generated by Django 3.0.3 on 2021-04-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riceapp', '0031_people_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('USER', 'USER')], default='user', max_length=50),
        ),
    ]
