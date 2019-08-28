import requests
from bs4 import BeautifulSoup
from typing import Callable

from custom_exceptions import RequestFailedException, WebsiteNotSupported
from requests_handler import perform_request
from custom_constants import *
import logging

module_logger = logging.getLogger('JustAnotherPriceChecker.price_checker')


def website_function_selector(website_name: str):
    switch = {
        'Amazon': check_amazon_price
    }
    return switch.get(website_name, default)


def update_current_prices_dictionary(title: str, price: float, currency: str, **kwargs):
    if len(title)>16:
        title = title[0:15]
    kwargs[CURRENT_PRICES][title] = str(price) + " " + currency


def amazon_page_parser(web_page):
    # read title and price from amazon page
    page_content = BeautifulSoup(web_page.content, 'html.parser')

    price = page_content.find(id=ID_AMAZON_PRICE)
    if price is None:
        price = page_content.find(id=ID_AMAZON_VENDOR_PRICE).contents[1].contents[2]  # secondary vendors price
    price = price.get_text()
    title = page_content.find(id=ID_AMAZON_PRODUCT_PRICE).get_text()
    title = title.strip()
    price, currency = price.split()
    price = price.replace(',', '.')
    price = float(price)
    return title, price, currency


def check_amazon_price(url: str, required_price: float, action_to_perform: Callable[[dict], None], **kwargs: dict):
    module_logger.info('Performing get request...')

    try:
        web_page = perform_request(url, requests.get)
    except RequestFailedException as requestFailedException:
        module_logger.error(requestFailedException.message)
        return

    title, price, currency = amazon_page_parser(web_page)

    update_current_prices_dictionary(title, price, currency, **kwargs)
    if price <= required_price:
        # set up values to be inserted in the notification
        kwargs[TITLE] = title
        kwargs[PRICE] = str(price) + " " + currency
        kwargs[URL] = url

        action_to_perform(**kwargs)


def default():
    raise WebsiteNotSupported
