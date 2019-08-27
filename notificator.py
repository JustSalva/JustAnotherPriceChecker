from custom_exceptions import NotificationMethodNotPresent


def notification_function_selector(notification_method_name: str):
    switch = {
        "IFTTT": send_IFTTT_notification
    }
    return switch.get(notification_method_name, default_notification)


def send_IFTTT_notification():
    pass


def default_notification():
    raise NotificationMethodNotPresent
