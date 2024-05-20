import requests
import json
import csv

url = "https://www.helloasso.com/algolia/1/indexes/*/queries"
headers = {
    "X-Algolia-Api-Key": "980128990635aaa7c2595b668df87497",
    "X-Algolia-Application-Id": "KOCVQI75M9",
    "Content-Type": "application/json",
    "x-algolia-agent": "Algolia for JavaScript (4.20.0); Browser",
    "Referer": "https://www.helloasso.com/e/recherche?tab=associations&bbox=-2.2578782727342457,47.807525990004905,-0.7948741407737714,48.561623479759874"
}


filters =  'place_city:"Pordic" AND place_department:"Côtes-d\'Armor"'
hits_per_page = 3

initial_data = {
    "requests": [
        {
            "indexName": "prod_organizations",
            "hitsPerPage": hits_per_page,
            "query": "",
            "filters": filters,
            "page": 0
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(initial_data)).json()
max_pages = response['results'][0]['nbPages']

with open('urls_associations.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['URL'])

    for page in range(max_pages):
        data = {
            "requests": [
                {
                    "indexName": "prod_organizations",
                    "hitsPerPage": hits_per_page,
                    "query": "",
                    "page": page,
                    "filters": filters,
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data)).json()
        hits = response['results'][0]['hits']

        for hit in hits:
            csvwriter.writerow([hit['url']])
