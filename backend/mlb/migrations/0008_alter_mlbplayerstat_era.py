# Generated by Django 5.1.5 on 2025-03-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0007_alter_mlbplayerstat_avg_alter_mlbplayerstat_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlbplayerstat',
            name='era',
            field=models.FloatField(null=True),
        ),
    ]
