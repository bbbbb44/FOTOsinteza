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
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        name = directory + '/' +  url.replace("/","")
        with open(name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def spider(plants):
    http = httplib2.Http()
    for j in range (0,len(plants)):
        try:
            os.mkdir(plantsNames[j])
        except:
            print("Couldnt create directory")
        status, response = http.request('https://garden.org/plants/view/' + plants[j])
        for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('img')):
            if link.has_attr('class'):
                if(link['class'] == ['plant_thumbimage'] and link['height']=="175"):
                    print(link)
                    download_web_image("https://garden.org" + link['src'].replace("-175",""), plantsNames[j])


if __name__ == "__main__":
    plants = ["181473", "181474"]
    plantsNames = ["Daylilies", "Iris"]
    x = spider(plants)

