# Generated by Django 2.1.2 on 2018-12-01 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_remove_project_accepted_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='accepted_bid',
            field=models.IntegerField(default=0),
        ),
    ]
