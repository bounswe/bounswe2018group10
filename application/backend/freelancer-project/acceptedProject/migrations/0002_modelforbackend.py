# Generated by Django 2.1.2 on 2018-11-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceptedProject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelForBackend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freelancer_id', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]
