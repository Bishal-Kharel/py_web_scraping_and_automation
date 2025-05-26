from datetime import datetime
from itertools import product
import requests
import csv
import bs4
import concurrent.futures
from tqdm import tqdm

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
REQUEST_HEADER = {
    'User-Agent' : USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}

NO_THREADS = 10

def get_page_html(url):
    res= requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price-whole'
    })

    if main_price_span:
        price = main_price_span.text.strip().replace(",", "")
        return price
    else:
        print("⚠️ Price not found.")
        return "N/A"

def get_product_title(soup):
        product_title = soup.find('span', id = 'productTitle')
        return product_title.text.strip()

def get_product_rating(soup):
    product_ratings_div = soup.find('div', attrs={
        'id': 'averageCustomerReviews'
    })
    product_rating_section = product_ratings_div.find('i', class_='a-icon-star')
    product_rating_span = product_rating_section.find('span')
    try:
        rating = product_rating_span.text.strip().split()
        return float(rating[0])
    except ValueError:
        print("Value Obtainned for Rating could not parsed")

def get_product_technical_details(soup):
    details ={}
    technical_details_section = soup.find('div', id='prodDetails')
    data_table = technical_details_section.find_all('table', id="productDetails_techSpec_section_1")

    for table in data_table:
        table_rows = table.find_all('tr')
        for row in table_rows:
            row_key =row.find('th').text.strip()
            row_value = row.find('td').text.strip().replace('\u200e', '')
            details[row_key]= row_value
    return details

def extract_product_info(url, output):
    product_info = {}
    # print (f'Scraping URl: {url}')
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['title'] = get_product_title(soup)
    product_info['price'] = get_product_price(soup)
    product_info['rating'] = get_product_rating(soup)
    product_info.update(get_product_technical_details(soup))
    output.append(product_info)

if __name__ =="__main__":
    products_data =[]
    urls =[]
    with open("amazon_products_urls.csv", newline="") as csvfile:
        urls = list(csv.reader(csvfile, delimiter=","))

    with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executer:
        for wkn in tqdm(range(0,len(urls))):
            executer.submit(extract_product_info, urls[wkn][0], products_data)
    output_file_name ='output-{}.csv'.format(datetime.today().strftime("%m-%d-%Y"))
    with open(output_file_name,'w') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerow(products_data[0].keys())
        for products in products_data:
            writer.writerow(products.values())