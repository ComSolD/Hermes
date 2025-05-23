# Generated by Django 5.1.5 on 2025-02-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0006_alter_nhlmatch_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NHLUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Обновление NHL',
                'verbose_name_plural': 'Обновления NHL',
                'db_table': 'nhl_update',
            },
        ),
    ]
