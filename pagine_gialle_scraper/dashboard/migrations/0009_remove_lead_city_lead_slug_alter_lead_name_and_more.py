# Generated by Django 4.2.1 on 2023-05-16 12:54

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_searchleads_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='city',
        ),
        migrations.AddField(
            model_name='lead',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, populate_from='name', primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lead',
            name='name',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='activity_type',
            field=models.CharField(default='ristorante', max_length=200, verbose_name='Tipo attività'),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='city',
            field=models.CharField(default='Milano', max_length=200, verbose_name='Città'),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='name',
            field=models.CharField(default='Search', max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='region',
            field=models.CharField(default='Lombardia', max_length=200, verbose_name='Regione'),
        ),
    ]