# search index uploads
from algoliasearch.search_client import SearchClient
from tqdm import tqdm
import os
import json
import requests
import time

print("Welcome to the GitaSearch uploader")
print("Training Gita... ")
client = SearchClient.create('STQEYSRJIF', os.environ['SEARCH_API'])
index = client.init_index('the_gita')

shlokas = [
    "47",
    "72",
    "43",
    "42",
    "29",
    "47",
    "30",
    "28",
    "34",
    "42",
    "55",
    "20",
    "35",
    "27",
    "20",
    "24",
    "28",
    "78"
]
for x in tqdm(range(1, 19)):
    for y in tqdm(range(1, int(shlokas[x-1]) + 1)):
        chap =str(x)
        shlok = str(y)
        try:
            headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
            }

            data = {
                'client_id': os.environ['client_id'],
                'client_secret': os.environ['client_secret'],
                'grant_type': 'client_credentials',
                'scope': 'verse chapter',
            }

            response = requests.post('https://bhagavadgita.io/auth/oauth/token', headers=headers, data=data)
            
            headers = {
                'accept': 'application/json',
            }

            params = {
                'access_token': response.json()["access_token"],
            }
            response = requests.get('https://bhagavadgita.io/api/v1/chapters/' + chap + '/verses/' + shlok, params=params, headers=headers)
            resultjson = {
                    "script": response.json()["transliteration"],
                    "meaning": response.json()["meaning"],
                    "chapter": chap,
                    "shloka": shlok
                }
            index.save_objects([{shlok: resultjson}],  {'autoGenerateObjectIDIfNotExist': True})
        except:
            print("Using Backup source " + chap + "." + shlok)
            response = requests.get('https://bhagavadgitaapi.in/slok/' + chap + '/' + shlok)
            resultjson = {
                "script": response.json()["transliteration"],
                "meaning": response.json()["purohit"]["et"],
                "chapter": chap,
                "shloka": shlok
            }
            index.save_objects([{shlok: resultjson}],  {'autoGenerateObjectIDIfNotExist': True})
