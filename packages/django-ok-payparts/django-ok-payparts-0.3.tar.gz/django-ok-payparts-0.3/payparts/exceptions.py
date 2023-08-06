__all__ = (
    'Error',
    'InvalidAuthDataError',
)


class Error(AttributeError):
    pass


class InvalidAuthDataError(Error):
    def __init__(self, code, message):
        self.code = code
        self.message = message
