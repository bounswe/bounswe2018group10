# Generated by Django 2.1.2 on 2018-11-07 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='file',
            field=models.FileField(blank=True, upload_to='files/'),
        ),
        migrations.AddField(
            model_name='project',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=7, default=None, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=7, default=None, max_digits=10, null=True),
        ),
    ]
