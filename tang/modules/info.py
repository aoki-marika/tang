class InfoModule:
    """
    The "info" module for a controller, responsible for providing metadata about
    the environment and program.
    """

    def __init__(self):
        self.requires_encryption = False

    def avs(__self__):
        """
        Get information about the Arcade Virtual System (AVS) module.
        """

        return [
            {
                'model': 'model',
                'ext': '-1',
                'dest': 'dest',
                'spec': 'spec',
                'rev': 'rev',
                'services': 'services',
                'version': 'version',
            },
        ]

    def launcher(__self__):
        """
        Get information about Spice.
        """

        return [
            {
                'version': 'version',
                'compile_date': 'compile_date',
                'compile_time': 'compile_time',
                'system_time': 'system_time',
                'args': ['args', 'args', 'args'],
            },
        ]
