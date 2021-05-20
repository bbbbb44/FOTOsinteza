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
    for plant in plants:
        try:
            os.mkdir(plant)
        except:
            print("Couldnt create directory")
        status, response = http.request('https://garden.org/plants/group/' + plant)
        for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('li')):
            if link.has_attr('data-thumb'):
                print(link['data-thumb'])
                download_web_image("https://garden.org" + link['data-thumb'].replace("-100",""), plant)


if __name__ == "__main__":
    plants = ["daylilies", "salvias", "sempervivum", "beets"]
    x = spider(plants)

