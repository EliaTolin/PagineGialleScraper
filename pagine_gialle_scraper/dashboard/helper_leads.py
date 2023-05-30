import json
from .models import Lead
from django.db.models import Count

def clear_search_leads_duplicate(search_leads):
    leads = Lead.objects.filter(search_leads=search_leads)
    email_set = set()  # Set per tenere traccia delle email già presenti
    # Lista dei lead da eliminare
    leads_to_delete = []
    for lead in leads:
        if lead.email in email_set:
            leads_to_delete.append(lead)
        else:
            email_set.add(lead.email)
    # Elimina i lead duplicati
    for lead in leads_to_delete:
        lead.delete()

def serialize_leads_to_dict(leads):
        result = []
        for l in leads:
            data = {}
            data['name'] = l.name
            data['email'] = l.email
            data['telephone'] = l.telephone
            data['city'] = l.city
            data['address'] = l.address
            data['activity_type'] = l.activity_type
            data['star'] = l.star
            result.append(data)
        return result
    
def serialize_leads_to_json(leads):
    return json.dumps(serialize_leads_to_dict(leads))
    