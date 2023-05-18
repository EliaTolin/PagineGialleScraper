# Generated by Django 4.2.1 on 2023-05-18 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0013_alter_lead_options_alter_searchoptions_activity_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchleads',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]