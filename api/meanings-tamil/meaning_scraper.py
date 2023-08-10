# Scrape all meanings - tamil
# These meanings are scraped from https://temple.dinamalar.com/bhagavad_gita_main.php

import requests
from bs4 import BeautifulSoup
import re


print("Scraped all links for chapters!\n")
x = input("What is the desired chapter to scrape from? (number from 1-18) >>> ")
print("Scraping...")
URL = "https://www.sangatham.com/bhagavad_gita/gita-chapter-" + x
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

all = soup.find_all("p")
firstshlok = soup.find_all("p", class_="Sloka")
del all[:all.index(firstshlok[0])]

for i in range(1, 79):
    try:
        if firstshlok[i].find_next_sibling() in firstshlok:
            print(firstshlok[i].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling())
        else:
            print(firstshlok[i].find_next_sibling().find_next_sibling().find_next_sibling())
    except IndexError:
        print("operation complete!")
        break