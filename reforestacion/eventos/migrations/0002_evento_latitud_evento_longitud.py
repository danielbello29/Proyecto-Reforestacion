# Generated by Django 5.1.1 on 2024-10-05 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='latitud',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='longitud',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
