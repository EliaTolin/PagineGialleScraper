# Generated by Django 4.2.1 on 2023-05-16 12:55

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_remove_lead_city_lead_slug_alter_lead_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', primary_key=True, serialize=False),
        ),
    ]
