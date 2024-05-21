import requests
import json
import csv
from bs4 import BeautifulSoup
import re
import datetime

# Initialize colorama for console colorization
from colorama import Fore, Style, init
init()

def get_config():
    return {
        "url": "https://www.helloasso.com/algolia/1/indexes/*/queries",
        "api_key": "980128990635aaa7c2595b668df87497",
        "app_id": "KOCVQI75M9",
        "referer": "https://www.helloasso.com/e/recherche?tab=associations",
        "insideBoundingBox": "", # Hitbox des assoss sur la carte (exemple: "[[48.40270693939982,-3.148647261719873,48.73711218710261,-2.4949607382821455]]")
        "filters": 'place_city:"Pordic" AND place_department:"Côtes-d\'Armor"',  # Pour tester a petite echelle
        "hits_per_page": 3 # De 1 à 1000
    }

def log_message(message_type, url, elapsed_time):
    now = datetime.datetime.now()
    time_str = now.strftime('[%Y-%m-%d %H:%M:%S]')
    types = {
        "info": Fore.GREEN,
        "warn": Fore.YELLOW,
        "error": Fore.RED
    }
    type_color = types.get(message_type, Fore.WHITE)
    print(f"{Fore.CYAN}{time_str}{type_color}[{message_type.upper()}]{Fore.BLUE}[{url}]{Fore.MAGENTA}[{elapsed_time:.2f} sec]{Style.RESET_ALL}")

def extract_contact_info(url):
    start_time = datetime.datetime.now()
    response = requests.get(url)
    elapsed_time = datetime.datetime.now() - start_time
    elapsed_seconds = elapsed_time.total_seconds()
    if response.ok:
        log_message("info", url, elapsed_seconds)
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'email' in script.string and 'phoneNumber' in script.string:
                match = re.search(r'contact:{email:"([^"]+)",phoneNumber:"([^"]+)"}', script.string)
                if match:
                    return match.groups()
    else:
        log_message("error", url, elapsed_seconds)
    return None, None

def fetch_data(page, config):
    start_time = datetime.datetime.now()
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
    elapsed_time = datetime.datetime.now() - start_time
    elapsed_seconds = elapsed_time.total_seconds()
    if response.ok:
        #log_message("info", config['url'], elapsed_seconds)
        return response.json()
    else:
        log_message("error", config['url'], elapsed_seconds)
        return None

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
