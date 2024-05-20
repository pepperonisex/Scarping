import requests
import json

url = "https://www.helloasso.com/algolia/1/indexes/*/queries"
headers = {
    "X-Algolia-Api-Key": "980128990635aaa7c2595b668df87497",
    "X-Algolia-Application-Id": "KOCVQI75M9",
    "Content-Type": "application/json",
    "x-algolia-agent": "Algolia for JavaScript (4.20.0); Browser",
    "Referer": "https://www.helloasso.com/e/recherche?tab=associations&bbox=-2.2578782727342457,47.807525990004905,-0.7948741407737714,48.561623479759874"
}

data = {
    "requests": [
        {
            "indexName": "prod_organizations",
            "hitsPerPage": 3,
            "query": "",
            "page": "",
            "insideBoundingBox": "",
            "filters": 'place_city:"Pordic" AND place_department:"Côtes-d\'Armor"',
            "params": ""
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data)).json()

urls = [hit['url'] for hit in response['results'][0]['hits']]
for url in urls:
    print(url)
