import requests
import json
import csv
from colorama import Fore, Style, init

init()

def get_config():
    """Retrieve configuration settings for the application."""
    return {
        "url": "https://www.helloasso.com/algolia/1/indexes/*/queries",
        "api_key": "980128990635aaa7c2595b668df87497",
        "app_id": "KOCVQI75M9",
        "referer": "https://www.helloasso.com/e/recherche?tab=associations&bbox=-2.2578782727342457,47.807525990004905,-0.7948741407737714,48.561623479759874",
        "filters": '',
        "hits_per_page": 1000
    }

def fetch_data(page, config):
    """Fetch data from Algolia API."""
    headers = {
        "X-Algolia-Api-Key": config['api_key'],
        "X-Algolia-Application-Id": config['app_id'],
        "Content-Type": "application/json",
        "x-algolia-agent": "Algolia for JavaScript (4.20.0); Browser",
        "Referer": config['referer']
    }
    data = {
        "requests": [
            {
                "indexName": "prod_organizations",
                "hitsPerPage": config['hits_per_page'],
                "query": "",
                "filters": config['filters'],
                "page": page
            }
        ]
    }
    print(Fore.CYAN + f"Fetching data for page {page}..." + Style.RESET_ALL)
    response = requests.post(config['url'], headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(Fore.GREEN + "Data fetched successfully." + Style.RESET_ALL)
        return response.json()
    else:
        print(Fore.RED + f"Error fetching data for page {page}: {response.status_code}, {response.text}" + Style.RESET_ALL)
        return None

def write_to_csv(hits):
    """Write the hits to a CSV file."""
    print(Fore.GREEN + "Writing to CSV file..." + Style.RESET_ALL)
    with open('urls_associations.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for hit in hits:
            csvwriter.writerow([hit['url']])
    print(Fore.GREEN + "Data written to CSV successfully." + Style.RESET_ALL)

def main():
    config = get_config()
    initial_response = fetch_data(0, config)
    if initial_response:
        max_pages = initial_response['results'][0]['nbPages']
        with open('urls_associations.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['URL'])

        for page in range(max_pages):
            response = fetch_data(page, config)
            if response and 'results' in response and len(response['results']) > 0:
                hits = response['results'][0]['hits']
                write_to_csv(hits)
            elif response is None:
                print(Fore.YELLOW + f"Stopping execution due to fetch error at page {page}." + Style.RESET_ALL)
                break

if __name__ == "__main__":
    main()
