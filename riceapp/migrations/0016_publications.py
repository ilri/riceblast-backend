# Generated by Django 3.0.3 on 2021-03-13 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riceapp', '0015_remove_fungalcollectionsite_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('publication', models.FileField(upload_to='Publications/publication')),
            ],
        ),
    ]
