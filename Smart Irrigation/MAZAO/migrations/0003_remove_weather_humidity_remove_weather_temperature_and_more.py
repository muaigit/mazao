# Generated by Django 5.1.5 on 2025-02-06 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAZAO', '0002_weather_willitraintommorow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='humidity',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='temperature',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='weatherDescription',
        ),
    ]
