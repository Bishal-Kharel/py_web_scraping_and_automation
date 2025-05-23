from datetime import datetime
import requests
import csv
import bs4

from api_scraper.remoteok_scraper import REQUEST_HEADER

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
REQUEST_HEADER = {
    'User-Agent' : USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}

def get_page_html(url):
    res= requests.get(url=url, headers=)

def extract_product_inf0(url):
    product_info = {}
    print (f'Scarping URl: {url}')
    html = 

if __name__ =="__main__":

    with open("amazon_products_urls.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            url = row[0]
            print(url)