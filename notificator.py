from custom_exceptions import NotificationMethodNotPresent
import requests

from custom_exceptions import RequestFailedException
from requests_handler import perform_request
import logging

module_logger = logging.getLogger('JustAnotherPriceChecker.notificator')
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'


def notification_function_selector(notification_method_name: str):
    switch = {
        "IFTTT": send_IFTTT_notification
    }
    return switch.get(notification_method_name, default_notification)


def send_IFTTT_notification(**kwargs):
    notification_key = kwargs['notification_key']
    event_name = kwargs['event_name']
    ifttt_webhook_url = IFTTT_WEBHOOKS_URL.format(event_name, notification_key)

    json_data = {
        "value1": kwargs["title"],
        "value2": kwargs["price"],
        "value3": kwargs["url"],
    }
    try:
        perform_request(ifttt_webhook_url, requests.post, data=json_data)
    except RequestFailedException as requestFailedException:
        module_logger.error(requestFailedException.message)


def default_notification():
    raise NotificationMethodNotPresent
