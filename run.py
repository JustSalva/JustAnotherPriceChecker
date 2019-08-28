#!/usr/bin/python3

import logging
import json
import time
from price_checker import *
from notificator import *
import traceback

logger = logging.getLogger("JustAnotherPriceChecker")
logger.setLevel(logging.DEBUG)

json_file_path = "./config.json"


def read_json_config_file():
    global amazon_urls_to_be_monitored_list, IFTTT_key, time_interval_between_requests,notification_method, kwargs
    with open(json_file_path, "r") as configuration_file:
        configuration_data = json.load(configuration_file)
    amazon_urls_to_be_monitored_list = configuration_data['urls_to_be_monitored_list']
    notification_method = configuration_data['notification_method']
    time_interval_between_requests = configuration_data['time_interval_between_requests']
    kwargs = configuration_data


if __name__ == '__main__':

    try:
        while True:
            read_json_config_file()
            for element_to_be_monitored in amazon_urls_to_be_monitored_list:
                url = element_to_be_monitored['url']
                required_price = element_to_be_monitored['required_price']
                website_name = element_to_be_monitored['website']

                website_function = website_function_selector(website_name)
                notification_function = notification_function_selector(notification_method)
                website_function(url, required_price, notification_function, **kwargs)

            time.sleep(time_interval_between_requests)
    except WebsiteNotSupported as websiteNotSupported:
        print(websiteNotSupported.message)
    except NotificationMethodNotPresent as notificationMethodNotPresent:
        print(notificationMethodNotPresent.message)
    except KeyboardInterrupt:
        print('Process Interrupted!')
    except Exception as e:
        print('Critical failure!')
        traceback.print_exc()
        send_failure_notification(**kwargs)
