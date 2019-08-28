from typing import Callable
import requests
from custom_exceptions import RequestFailedException
from custom_constants import *
import logging

module_logger = logging.getLogger('JustAnotherPriceChecker.requests_handler')

HEADERS = {
    'User-Agent': CHROME_USER_AGENT
}


def perform_request(url, requests_function: Callable, data=None):
    try:
        if data is not None:
            web_page = requests_function(url, headers=HEADERS, json=data)
        else:
            web_page = requests_function(url, headers=HEADERS)
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
