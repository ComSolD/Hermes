# Generated by Django 5.1.5 on 2025-01-29 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0006_rename_total_q1missed_nbateamptsstat_total_q1_missed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='ast',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='attempted_three_pt',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='blk',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='dreb',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='fg',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='ft',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='oreb',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='pf',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='plus_minus',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='pts',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='reb',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='stl',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='three_pt',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='trying_fg',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='trying_ft',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbaplayerstat',
            name='turnovers',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='ast',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='attempted_three_pt',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='blk',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='dreb',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='fg',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='ft',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='oreb',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='pf',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='reb',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='stl',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='three_pt',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='trying_fg',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='trying_ft',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nbateamstat',
            name='turnovers',
            field=models.IntegerField(null=True),
        ),
    ]
