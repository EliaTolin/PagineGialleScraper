# Generated by Django 4.2.1 on 2023-05-16 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_searchleads_list_results_lead_search_leads'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchoptions',
            name='name',
            field=models.CharField(default='', max_length=200, verbose_name='Nome'),
            preserve_default=False,
        ),
    ]
