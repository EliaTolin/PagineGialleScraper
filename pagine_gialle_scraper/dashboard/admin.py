from django.contrib import admin

# Register your models here.
from .models import SearchLeads, Lead

admin.site.register(SearchLeads)
admin.site.register(Lead)
