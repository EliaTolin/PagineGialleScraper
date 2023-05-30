import json
from django.http import  HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from dashboard.filters import LeadFilter
from dashboard.helper_leads import serialize_leads_to_dict, serialize_leads_to_json
from .task.celery_tasks import *
from .forms import SearchForms
from .models import *
from datetime import datetime
from django.core.cache import cache
import pandas as pd
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

def index(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        # Leggi il contenuto del file JSON
        json_data = json.load(json_file)
        cache.set('json_data', json_data)
        return redirect('dashboard:search_form')

    last_search = SearchLeads.objects.filter(user=request.user)
    context = {'form': SearchForms(), 'last_search': last_search}
    return render(request, 'dashboard/index.html', context)

def search_form(request, json_data=None):
    initial_data = {}
    json_data = cache.get('json_data')
    cache.delete('json_data')
    if json_data:
        try:
            city_list = json_data.get('city', [])
            initial_data['city'] = ', '.join(city_list) 
            activity_type = json_data.get('activity_type', [])
            initial_data['activity_type'] = ', '.join(activity_type)
        except json.JSONDecodeError:
            return HttpResponse("Errore: I dati JSON non sono validi.")
    initial_data['region'] = request.user.region
    form = SearchForms(request.POST or None, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        search = form.save()
        search_leads = SearchLeads.objects.create(
            name=search.name,
            search_date=datetime.now(),
            search_options=search,
            finished=False,
            user=request.user
        )
        search_leads.save()
        start_search(search_leads.slug,search.exclude_no_email)
        return redirect("dashboard:index")

    context = {'form': form}
    return render(request, 'dashboard/new_search.html', context)

class SearchLeadsDetail(generic.DetailView):
    model = SearchLeads
    template_name = "dashboard/detail.html"

    def get_context_data(self, **kwargs):
        search_leads = SearchLeads.objects.get(slug=self.kwargs['slug'])
        if search_leads.user != self.request.user:
            raise PermissionDenied("Accesso negato")
        leads = search_leads.lead_set.all()
        lead_filter = LeadFilter(self.request.GET, queryset=leads,leads=leads)
        if self.request.GET:
            leads = lead_filter.qs

        paginator = Paginator(leads, 25)
        page_number = self.request.GET.get('page')
        leads = paginator.get_page(page_number)
        
        len_leads = search_leads.lead_set.count()
        list_pages_navigator = []
        if page_number:
            page_number = int(page_number)
            if page_number > 1:
                list_pages_navigator.append(page_number - 1)
            list_pages_navigator.append(page_number)
            if page_number < paginator.num_pages:
                list_pages_navigator.append(page_number + 1)
            if page_number+1 < paginator.num_pages:
                list_pages_navigator.append(page_number + 2)
        else:
            list_pages_navigator.append(1)
            if paginator.num_pages > 1:
                list_pages_navigator.append(2)
            if paginator.num_pages > 2:
                list_pages_navigator.append(3)
                
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        query_string = query_params.urlencode()

        context = {'leads': leads,
                   'search_leads': search_leads,
                   'len_leads':len_leads,
                   'list_pages_navigator': list_pages_navigator,
                   'lead_filter': lead_filter,
                   'query_string':query_string,
                   'search_options':search_leads.search_options,
                   }
        return context

def delete_search(request, slug):
    search_leads = get_object_or_404(SearchLeads, slug=slug)
    if search_leads.user != request.user:
        return HttpResponse("Non hai i permessi per visualizzare questa pagina.")
    search_leads.delete()
    return redirect('dashboard:index')

def delete_lead(request, slug):
    lead = get_object_or_404(Lead, slug=slug)
    if lead.search_leads.user  != request.user:
        return HttpResponse("Non hai i permessi per visualizzare questa pagina.")
    lead.delete()
    return redirect('dashboard:index')

def star_lead(request, slug):
    lead = get_object_or_404(Lead, slug=slug)
    if lead.search_leads.user  != request.user:
        return HttpResponse("Non hai i permessi per visualizzare questa pagina.")
    lead.star = not lead.star
    lead.save()
    return redirect('dashboard:index')

def save_to_json_leads(request, slug):
    search_leads = get_object_or_404(SearchLeads, slug=slug)
    if search_leads.user != request.user:
        return HttpResponse("Non hai i permessi per visualizzare questa pagina.")
    data = serialize_leads_to_json(search_leads.lead_set.all())
    # Crea una risposta HTTP con il contenuto JSON
    response = JsonResponse(data, content_type='application/json',safe=False)
    response['Content-Disposition'] = 'attachment; filename="{0}.json"'.format(search_leads.name)
    return response

def save_to_csv_leads(request, slug):
    search_leads = get_object_or_404(SearchLeads, slug=slug)
    if search_leads.user != request.user:
        return HttpResponse("Non hai i permessi per visualizzare questa pagina.")
    leads = search_leads.lead_set.all()
    lead_filter = LeadFilter(request.GET, queryset=leads,leads=leads)
    leads = lead_filter.qs
    data = serialize_leads_to_dict(leads)
    df = pd.DataFrame(data)
    data_csv = df.to_csv(index=False)
    response = HttpResponse(data_csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(search_leads.name)
    return response
