# Generated by Django 5.1.5 on 2025-02-03 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0010_alter_nflmatch_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='nflmatch',
            name='season_type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
