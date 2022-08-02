class CaptureModule:
    """
    The "capture" module for a controller, responsible for providing access to
    and metadata about the various screens connected to the server.
    """

    def __init__(self):
        self.requires_encryption = False

    def get_screens(self):
        """
        Get the unique identifiers of each of the connected screens.
        """

        return [
            0,
            1,
        ]
