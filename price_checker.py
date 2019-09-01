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
        'Amazon': amazon_page_parser,
        'ResetDigitale': resetdigitale_page_parser
    }
    return switch.get(website_name, default)


def update_current_prices_dictionary(title: str, price: float, currency: str, **kwargs):
    if len(title) > 16:
        title = title[0:20]
    kwargs[CURRENT_PRICES][title] = str(price) + " " + currency


def resetdigitale_page_parser(web_page):
    # read title and price from amazon page
    page_content = BeautifulSoup(web_page.content, 'html.parser')

    price = page_content.find('span', {'class': 'price'}, id=ID_RESETDIGITALE_PRICE)
    price = price.get_text()
    title = page_content.find(id=ID_RESETDIGITALE_TITLE).get_text().split("  ", maxsplit=1)[0]
    title = title.strip()
    currency, price = price.split()
    price = float(price)
    return title, price, currency


def amazon_page_parser(web_page):
    # read title and price from amazon page
    page_content = BeautifulSoup(web_page.content, 'html.parser')

    price = page_content.find(id=ID_AMAZON_PRICE)
    if price is None:
        # secondary vendors price if Amazon's one is unavailable
        price = page_content.find(id=ID_AMAZON_VENDOR_PRICE_NEW_AND_USED)
        if price is None:  # if used price is not present, the array position changes
            price = page_content.find(id=ID_AMAZON_VENDOR_PRICE_ONLY_NEW)
        price = price.contents[1].contents[2]

    price = price.get_text()
    title = page_content.find(id=ID_AMAZON_PRODUCT_PRICE).get_text()
    title = title.strip()
    price, currency = price.split()
    price = price.replace(',', '.')
    price = float(price)
    return title, price, currency


def check_price(url: str, required_price: float, page_parser: Callable, action_to_perform: Callable[[dict], None],
                **kwargs: dict):
    module_logger.info('Performing get request...')

    try:
        web_page = perform_request(url, requests.get)
    except RequestFailedException as requestFailedException:
        module_logger.error(requestFailedException.message)
        return

    title, price, currency = page_parser(web_page)

    update_current_prices_dictionary(title, price, currency, **kwargs)
    if price <= required_price:
        # set up values to be inserted in the notification
        kwargs[TITLE] = title
        kwargs[PRICE] = str(price) + " " + currency
        kwargs[URL] = url

        action_to_perform(**kwargs)


def default():
    raise WebsiteNotSupported
