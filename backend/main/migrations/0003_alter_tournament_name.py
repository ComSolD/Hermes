# Generated by Django 5.1.5 on 2025-03-17 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_tournament_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(choices=[('NBA', 'NBA'), ('NHL', 'NHL'), ('NFL', 'NFL'), ('MLB', 'MLB')], max_length=100, unique=True),
        ),
    ]
