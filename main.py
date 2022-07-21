from bs4 import BeautifulSoup
import requests
import re


def find_prices():
    """
    example data

    {
        "product_title": "Serkan",
        "prices": [
                    {
                        "company": "value",
                        "price": "value"
                    }, ...
                  ]
    }

    """
    url_for_web_page = "https://www.cimri.com/cep-telefonu"
    html_text = requests.get(
        url_for_web_page).text

    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('div', class_="z7ntrt-0 cLlfW s1a29zcm-11 ggOMjb")  # Div for product list
    bike_prices = []

    for product in products:
        product_info = dict()
        product_info['product_title'] = product.article.a['title']
        top_offers = product.find_all('a',
                                   class_="s14oa9nh-0 lihtyI")  # a for product prices inside of the div that founded previously
        prices = list()
        for offer in top_offers:
            price = dict()
            split_data_company_and_price = re.split('(\d+.\d+,\d+|\d+,\d+)',
                                                    offer.text)  # n11.com19.500,00 TL -- split the price and store name
            price["company"] = split_data_company_and_price[0]
            price["price"] = split_data_company_and_price[1]
            prices.append(price)
        product_info["prices"] = prices
        bike_prices.append(product_info)

    from pprint import pprint
    pprint(bike_prices)


find_prices()