import requests
from bs4 import BeautifulSoup
from typing import Callable

from custom_exceptions import RequestFailedException, WebsiteNotSupported
import logging

module_logger = logging.getLogger('JustAnotherPriceChecker.price_checker')

HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


def website_function_selector(website_name: str):
    switch = {
        "Amazon": check_amazon_price
    }
    return switch.get(website_name, default)


def perform_get_request(url):
    try:
        web_page = requests.get(url, headers=HEADERS)
    except requests.ConnectionError:
        module_logger.error('Cannot connect to the url due to network problem.')
    except requests.HTTPError:
        module_logger.error('Invalid HTTP response.')
    except requests.TooManyRedirects:
        module_logger.error('The request exceeds the maximum number of redirections.')
    except requests.Timeout:
        module_logger.error('The request timeout is expired.')
    else:
        return web_page

    raise RequestFailedException


def check_amazon_price(url: str, required_price: float, action_to_perform: Callable[[dict], None], **kwargs: dict):
    module_logger.info('Performing get request...')

    try:
        web_page = perform_get_request(url)
    except RequestFailedException as requestFailedException:
        module_logger.error(requestFailedException.message)
        return

    page_content = BeautifulSoup(web_page.content, 'html.parser')
    price = page_content.find(id='priceblock_ourprice').get_text()
    price, _ = price.split()
    price = price.replace(",", ".")
    price = float(price)
    if price <= required_price:
        action_to_perform(**kwargs)


def default():
    raise WebsiteNotSupported
