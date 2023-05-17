import time
import requests
from bs4 import BeautifulSoup
import json
import csv
import argparse
import os
import pandas as pd

# URL = "https://www.paginegialle.it/lombardia/basiglio/idraulici.html"

URL = "https://www.paginegialle.it/{0}/{1}/{2}.html"
header = ['nome', 'email', 'telefono', 'citta', 'via', 'tipo_attivita']


def scraper(output: str, regione: str, citta: str, keyword: str, append: bool, exclude_no_email: bool):
    scraper_URL = URL.format(regione, citta, keyword)

    if append:
        f = open(output, "a")
    else:
        f = open(output, "w")
    writer = csv.writer(f)

    if not append or os.stat(output).st_size == 0:
        writer.writerow(header)
    try:
        page = requests.get(scraper_URL)
    except:
        print("ERROR")
        exit(-1)
    soup = BeautifulSoup(page.content, "html.parser")
    dataTag = soup.find_all('script', type='application/ld+json')
    if len(dataTag) == 0:
        print("NESSUN RISULTATO TROVATO")
        return
    json_text = dataTag[1].text
    data = json.loads(json_text)
    number_results = 0
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
        if append:
            writer = csv.writer(f)
        number_results += 1
        writer.writerow([name, email, telephone, citta, via, keyword])

    print("TROVATI {0} RISULTATI!".format(number_results))


def from_config_file(arguments):
    f = open(arguments.config_file)
    config = json.load(f)

    for citta in config['citta']:
        for keyword in config['keyword']:
            print("SCRAPING IN {0} PER {1}".format(citta, keyword))
            scraper(arguments.output, arguments.regione, citta, keyword, True, arguments.exclude_no_email)
            time.sleep(3)


def clear_file(file_name):
    print("Pulisco il file")
    df = pd.read_csv(file_name, sep=",")
    df = df.drop_duplicates(subset="email")
    output_filename = "{0}_cleaned.csv".format(os.path.splitext(file_name)[0])
    df.to_csv(output_filename, index=False)
    print("Salvato in {0}".format(output_filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scraper Pagine Gialle, lo spazio si converte in _ esempio : emilia_romagna')

    parser.add_argument('-o', '--output', type=str, default='output.csv',
                        help='Nome del file CSV di output (default: output.csv)')

    parser.add_argument('-c', '--citta', type=str, default='milano',
                        help='Citta di scraping (default: milano)')

    parser.add_argument('-r', '--regione', type=str, default='lombardia',
                        help='Regione di scraping (default: lombardia)')

    parser.add_argument('-k', '--keywords', type=str, default='idraulico',
                        help='Keywords di ricerca (default: idraulico)')

    parser.add_argument('-a', '--append', type=bool, const=True, default=False, nargs='?',
                        help='Append nel file')

    parser.add_argument('-e', '--exclude_no_email', type=bool, const=True, default=False, nargs='?',
                        help='Esclude i lead senza email')

    parser.add_argument('-cf', '--config_file', type=str, default=None,
                        help='File con keyword e citta')

    parser.add_argument('-cl', '--clear', type=bool, const=True, default=False, nargs='?',
                        help='Pulisce il risultato da doppioni')

    parser.add_argument('-ocl', '--only_clear', type=bool, const=True, default=False, nargs='?',
                        help='Pulisce un file di output e termina')

    args = parser.parse_args()

    if args.only_clear:
        clear_file(args.output)
        exit()

    if args.config_file is None:
        scraper(args.output, args.regione, args.citta, args.keywords, args.append, args.exclude_no_email)
    else:
        from_config_file(args)

    if args.clear:
        clear_file(args.output)

    print("Finito!")
