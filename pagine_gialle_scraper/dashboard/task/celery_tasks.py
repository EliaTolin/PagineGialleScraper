import time
from celery import shared_task, current_task
from celery.exceptions import *
from dashboard.scraper import scraper
from ..models import SearchLeads,Lead
from dashboard.helper_leads import clear_search_leads_duplicate

@shared_task(bind=True)
def scraper_task(self, *args, **kwargs):
    try:
        search_leads = SearchLeads.objects.get(slug=kwargs['slug'])
        exclude_no_email = kwargs['exclude_no_email']
        search_options = search_leads.search_options
        
        list_city = search_options.get_city_list()
        list_activity_type = search_options.get_activity_type_list()
        
        for city in list_city:
            for activity in list_activity_type:
                current_task.update_state(state='PROGRESS', meta={'current': city, 'total': len(list_city)})
                list_result = scraper.scraper(search_options.region, city, activity, search_options.exclude_no_email)
                if list_result is None:
                    continue
                for lead in list_result:
                    lead = Lead.objects.create(name= lead.name, email=lead.email, telephone=lead.telephone, city=lead.city,\
                        address=lead.address, activity_type=lead.activity_type, search_leads=search_leads)
                    lead.save()
        if exclude_no_email:      
            clear_search_leads_duplicate(search_leads)
        search_leads.finished = True
        search_leads.save()
    except Exception as e:
        exc_info = e
        raise e
    
def start_search(slug,exclude_no_email):
    task = scraper_task.delay(slug=slug,exclude_no_email=exclude_no_email)
    print(task.status)
    