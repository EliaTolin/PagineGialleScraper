import time
import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import pandas as pd
from ..models import Lead, SearchLeads

URL = "https://www.paginegialle.it/{0}/{1}/{2}.html"
header = ['nome', 'email', 'telefono', 'citta', 'via', 'tipo_attivita']

class ResultScraping:
    def __init__(self, name, email, telephone, city, address, activity_type):
        self.name = name
        self.email = email
        self.telephone = telephone
        self.city = city
        self.address = address
        self.activity_type = activity_type
    


def scraper(regione: str, citta: str, keyword: str,exclude_no_email: bool):
    scraper_URL = URL.format(regione, citta, keyword)
    try:
        page = requests.get(scraper_URL)
    except:
        return None
    soup = BeautifulSoup(page.content, "html.parser")
    dataTag = soup.find_all('script', type='application/ld+json')
    if len(dataTag) == 0:
        return None
    json_text = dataTag[1].text
    data = json.loads(json_text)
    number_results = 0
    list_results = []
    for d in data['itemListElement']:
        item = d['item']
        name = item['name']
        email = None
        telephone = None

        citta = item['address']['addressLocality'] if 'addressLocality' in item['address'] else ""
        via = item['address']['streetAddress'] if 'streetAddress' in item['address'] else ""
        if 'contactPoint' not in item:
            continue
        for c in item['contactPoint']:
            email = c['email'] if "email" in c else ""
            telephone = c['telephone'] if "telephone" in c else ""

        if exclude_no_email and email == "":
            continue
        number_results += 1
        result = ResultScraping(name, email, telephone, citta, via, keyword)
        list_results.append(result)
    return list_results
