import json
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.core import serializers

from accounts.models import UserProfile

header = ['nome', 'email', 'telefono', 'citta', 'via', 'tipo_attivita']


class SearchOptions(models.Model):
    name = models.CharField("Nome", max_length=200)
    city = models.CharField("Città", max_length=500)
    region = models.CharField("Regione", max_length=200,default="emilia_romagna")
    activity_type = models.CharField("Tipo attività", max_length=500)
    exclude_no_email = models.BooleanField("Escludi senza email", default=True)
    
    #Get city list from field
    def get_city_list(self):
        return self.city.replace(" ", "").split(",")
    
    def get_activity_type_list(self):
        return self.activity_type.replace(" ", "").split(",")


class Lead(models.Model):
    name = models.TextField(max_length=200)
    email = models.EmailField(max_length=200, null=True)
    telephone = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(primary_key=True)
    address = models.CharField(max_length=200, null=True)
    activity_type = models.CharField(max_length=200, null=True)
    search_leads = models.ForeignKey('SearchLeads', on_delete=models.CASCADE, null=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name.replace(" ", "_")

class SearchLeads(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField("Nome", max_length=200)
    slug = AutoSlugField(populate_from='search_date',
                         unique=True)
    search_date = models.DateTimeField(primary_key=True)
    finished = models.BooleanField(default=False)
    search_options = models.ForeignKey(SearchOptions, on_delete=models.DO_NOTHING, null=True)
    
    def serialize_leads_to_json(self):
        leads = Lead.objects.filter(search_leads=self)
        result = []
        for l in leads:
            data = {}
            data['name'] = l.name
            data['email'] = l.email
            data['telephone'] = l.telephone
            data['city'] = l.city
            data['address'] = l.address
            data['activity_type'] = l.activity_type
            result.append(data)
        
        return json.dumps(result)
    
    def serialize_leads_to_dict(self):
        leads = Lead.objects.filter(search_leads=self)
        result = []
        for l in leads:
            data = {}
            data['name'] = l.name
            data['email'] = l.email
            data['telephone'] = l.telephone
            data['city'] = l.city
            data['address'] = l.address
            data['activity_type'] = l.activity_type
            result.append(data)
        
        return result
    
    def __str__(self):
        return self.name.replace(" ", "_")
    
    def get_absolute_url(self):
        return reverse("dashboard:search_detail", kwargs={"slug": self.slug})
    
    def get_status_string(self):
        return "FINITO" if self.finished else "IN CORSO"
