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


def json_data_parser(value1=None, value2=None, value3=None, occurred_at=None):
    json_data = dict()
    if value1 is not None:
        json_data['value1'] = value1

    if value2 is not None:
        json_data['value2'] = value2

    if value3 is not None:
        json_data['value3'] = value3

    if value3 is not None:
        json_data['occurredAt'] = occurred_at

    return json_data


def send_IFTTT_notification(**kwargs):
    event_name = kwargs['event_name']
    json_data = json_data_parser(value1=kwargs["title"], value2=kwargs["price"], value3=kwargs["url"])

    send_generic_notification(event_name, json_data=json_data, **kwargs)


def send_failure_notification(**kwargs):
    event_name = 'RaspberryServiceDown'
    json_data = json_data_parser(value1='JustAnotherPriceChecker')
    send_generic_notification(event_name, json_data=json_data, **kwargs)


def send_generic_notification(notification_name: str, json_data: dict = None, **kwargs):
    notification_key = kwargs['notification_key']
    ifttt_webhook_url = IFTTT_WEBHOOKS_URL.format(notification_name, notification_key)
    try:
        perform_request(ifttt_webhook_url, requests.post, data=json_data)
    except RequestFailedException as requestFailedException:
        module_logger.error(requestFailedException.message)

def send_weekly_report(**kwargs):
    event_name = 'WeeklyReport'
    json_data = json_data_parser(value1=kwargs[WEEKLY_REPORT])
    send_generic_notification(event_name, json_data=json_data, **kwargs)

def default_notification():
    raise NotificationMethodNotPresent
