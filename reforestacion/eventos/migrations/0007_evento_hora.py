# Generated by Django 5.1.1 on 2024-10-26 00:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0006_evento_participantes_alter_evento_lider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]