# Generated by Django 4.2.1 on 2023-05-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_searchleads_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='star',
            field=models.BooleanField(default=False),
        ),
    ]