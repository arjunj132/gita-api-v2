# This script is designed to scrape the Tamil JSON from the JSON here:
# https://raw.githubusercontent.com/gita/gita/feat--new-languages/data/transliteration.json
# These scripts are taken from the Gita project on Github, from a branch that hasen't been
# merged yet, so these scripts my have a few problems in them 
# count 6309

import requests
from tqdm import tqdm
import time
import json


def scrape(x1):
    fetched = False
    received_scripts = []
    for i in tqdm(range(6310)):
        if fetched == False:
            global r
            r = requests.get('https://raw.githubusercontent.com/gita/gita/feat--new-languages/data/transliteration.json')
            fetched = True
            tqdm.write("Fetched all scripts, starting to scrape...")
            time.sleep(1)
        else:
            if r.json()[i-1]["lang"] == x1:
                if r.json()[i-1]["verseNumber"] == 1:
                    tqdm.write("Recived first " + x1 + " script, index # " + str(r.json()[i-1]["id"]))
                received_scripts.append(r.json()[i-1]["description"])

    print("Successfully got scripts for " + x1 + "\n\n")
    x = input("Would you like to save this to a JSON file? (y/n) ")
    if x == "y":
        x = input("What would you like to name it? >>> ")
        with open(x+".json", "w") as output:
            json.dump(received_scripts, output, ensure_ascii=False)
    else:
        print("Operation complete!")

print("Language scraper - Gita API scraper of JSON scripts:\n\n")
print("Languages: https://raw.githubusercontent.com/gita/gita/feat--new-languages/data/languages.json")
x = input('Enter your language (case sensitive - "a" for all): ')

if x == "a":
    print("Getting all languages...")
    completelanglist = []
    langs = requests.get('https://raw.githubusercontent.com/gita/gita/feat--new-languages/data/languages.json')
    for i in langs.json():
        completelanglist.append(i["language"])
    for o in completelanglist:
        print("Starting scraping for "+ o)
        scrape(o)
else:
    print("\n\nSetting up and scraping - scripts for '" + x + "'")
    scrape(x)