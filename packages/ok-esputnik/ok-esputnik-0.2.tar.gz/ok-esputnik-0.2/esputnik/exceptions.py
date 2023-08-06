__all__ = (
    'Error',
    'InvalidAuthDataError',
    'IncorrectDataError'
)


class Error(AttributeError):
    pass


class InvalidAuthDataError(Error):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class IncorrectDataError(InvalidAuthDataError):
    pass
