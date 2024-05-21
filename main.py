import requests
import json
import csv
from bs4 import BeautifulSoup
import re

# Initialize colorama for console colorization
from colorama import Fore, Style, init
init()

def get_config():
    return {
        "url": "https://www.helloasso.com/algolia/1/indexes/*/queries",
        "api_key": "980128990635aaa7c2595b668df87497",
        "app_id": "KOCVQI75M9",
        "referer": "https://www.helloasso.com/e/recherche?tab=associations",
        "filters": 'place_city:"Pordic" AND place_department:"Côtes-d\'Armor"',
        "hits_per_page": 3
    }

def extract_contact_info(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'email' in script.string and 'phoneNumber' in script.string:
                match = re.search(r'contact:{email:"([^"]+)",phoneNumber:"([^"]+)"}', script.string)
                if match:
                    return match.groups()
    return None, None

def fetch_data(page, config):
    headers = {
        "X-Algolia-Api-Key": config['api_key'],
        "X-Algolia-Application-Id": config['app_id'],
        "Content-Type": "application/json",
        "x-algolia-agent": "Algolia for JavaScript (4.20.0); Browser",
        "Referer": config['referer']
    }
    data = {"requests": [{"indexName": "prod_organizations", "hitsPerPage": config['hits_per_page'],
                          "query": "", "filters": config['filters'], "page": page}]}
    response = requests.post(config['url'], headers=headers, data=json.dumps(data))
    return response.json() if response.ok else None

def write_to_csv(hits):
    with open('contact_info.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for hit in hits:
            url = hit['url']
            name = hit['name']
            email, phone_number = extract_contact_info(url)
            if email and phone_number:
                writer.writerow([name, email, phone_number])

def main():
    config = get_config()
    initial_response = fetch_data(0, config)
    if initial_response:
        max_pages = initial_response['results'][0]['nbPages']
        with open('contact_info.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nom', 'Email', 'Numéro de Téléphone'])

        for page in range(max_pages):
            response = fetch_data(page, config)
            if response:
                hits = response['results'][0]['hits']
                write_to_csv(hits)

if __name__ == "__main__":
    main()
