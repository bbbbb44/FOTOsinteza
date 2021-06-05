# This Python file uses the following encoding: utf-8
import sys
import requests
from bs4 import BeautifulSoup, SoupStrainer
import random
import httplib2
import urllib.request
import shutil
import os

def download_web_image(url, directory):
    r = requests.get(url, stream=True) # request za sliko
    if r.status_code == 200:
        name = directory + '/' +  url.replace("/","") # Sliko dam v direktory, ker pa ne sme imeti datoteka v imenu / samo replaceam z praznim stringom
        with open(name, 'wb') as f: # shranjevanje
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)



def is_number(s): # simpl funkcija za preverjanje če je številka
    try:
        float(s)
        return True
    except ValueError:
        return False

def spider(plants):
    http = httplib2.Http()
    for j in range (0,len(plants)):
        try:
            os.mkdir(plantsNames[j]) # Ustvarim direktorij z imenom
        except:
            print("Couldnt create directory")
        status, response = http.request('https://garden.org/plants/view/' + plants[j])
        for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('img')): # najdem vse slike
            if link.has_attr('class'):
                if(link['class'] == ['plant_thumbimage'] and link['height']=="175"): # Vse slike v databaseu ki me zanimajo so classa plant_thumbimage in heighta 175
                    print(link)
                    download_web_image("https://garden.org" + link['src'].replace("-175",""), plantsNames[j]) # Full sized sliko dobim da zamenjam -175 z praznim stringom.


if __name__ == "__main__":
    # med plants zapišeš številko database entry-ja npr https://garden.org/plants/view/228296
    plants = ["181506", "76165", "186377", "228296"]
    # med plantsNames pa na n-to mesto zapišeš ime kako naj bo tvoj entry poimenovan
    plantsNames = ["Roses", "Dalhias", "Sempervivum", "Salvias"]
    x = spider(plants)

