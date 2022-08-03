class ControllerException(BaseException):
    """
    An exception which occurs during the processing of a request to a Controller.
    """

    def __init__(self, message):
        self.message = message
