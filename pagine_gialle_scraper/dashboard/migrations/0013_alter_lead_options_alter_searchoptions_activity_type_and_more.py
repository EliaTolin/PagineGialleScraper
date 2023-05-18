# Generated by Django 4.2.1 on 2023-05-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_lead_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='activity_type',
            field=models.CharField(max_length=500, verbose_name='Tipo attività'),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='city',
            field=models.CharField(max_length=500, verbose_name='Città'),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='searchoptions',
            name='region',
            field=models.CharField(default='emilia_romagna', max_length=200, verbose_name='Regione'),
        ),
    ]
