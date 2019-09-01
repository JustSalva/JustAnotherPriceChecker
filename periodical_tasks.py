import json
from notificator import send_weekly_report
from custom_constants import *


def load_current_prices_file():
    with open("current_prices.json", "r") as current_prices_file:
        current_prices = json.load(current_prices_file)
    return current_prices


def weekly_report(kwargs=None):
    current_prices = load_current_prices_file()
    notification_body = "\n"
    for item in current_prices:
        notification_body = notification_body + item + ':\t' + current_prices[item] + '\n'
    kwargs[WEEKLY_REPORT] = notification_body
    send_weekly_report(**kwargs)
