""" Here there are all custom exceptions of the project"""


class GenericException(Exception):
    """Base class for all project's exceptions"""

    def __init__(self, message):
        self.message = message

    pass


class RequestFailedException(GenericException):
    def __init__(self):
        super().__init__("The request could not be performed")

    pass


class NotificationMethodNotPresent(GenericException):
    def __init__(self):
        super().__init__("The selected notification method is either not supported or it does not exist!")

    pass


class WebsiteNotSupported(GenericException):
    def __init__(self):
        super().__init__("The selected website is not supported, you may consider implement its module :)")

    pass
