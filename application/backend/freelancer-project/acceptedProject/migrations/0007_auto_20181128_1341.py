# Generated by Django 2.1.2 on 2018-11-28 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acceptedProject', '0006_auto_20181128_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptedproject',
            name='freelancer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='freelancer', to=settings.AUTH_USER_MODEL),
        ),
    ]
