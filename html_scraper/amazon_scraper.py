from datetime import datetime
import requests
import csv
import bs4

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
REQUEST_HEADER = {
    'User-Agent' : USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}

def get_page_html(url):
    res= requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price-whole'
    })

    if main_price_span:
        price = main_price_span.text.strip().replace(",", "")
        # print(f"💰 Price found: {price}")
        return price
    else:
        print("⚠️ Price not found.")
        return "N/A"

    # price_span = main_price_span.findAll('span')
    # for span in price_span:
    #     price = span.text.strip().replace("$","").replace(",","")
    #     print(price)


def extract_product_info(url):
    product_info = {}
    print (f'Scarping URl: {url}')
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    return product_info

if __name__ =="__main__":

    with open("amazon_products_urls.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            url = row[0]
            print(extract_product_info(url))