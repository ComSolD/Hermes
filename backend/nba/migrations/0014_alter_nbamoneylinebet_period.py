# Generated by Django 5.1.5 on 2025-03-01 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0013_nbateam_second_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nbamoneylinebet',
            name='period',
            field=models.CharField(choices=[('full_time', 'Весь Матч'), ('1st_half', '1-я Половина'), ('1st_quarter', '1-я Четверть'), ('2nd_quarter', '2-я Четверть'), ('2nd_half', '2-я Половина'), ('3rd_quarter', '3-я Четверть'), ('4th_quarter', '4-я Четверть')], max_length=20),
        ),
    ]
