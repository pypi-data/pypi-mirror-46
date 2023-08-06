class MasonError(RuntimeError):
    pass


# C
class ConnectionError(MasonError):
    pass


# E
class ExitException(MasonError):
    def __init__(self, code: int = 0):
        super().__init__()
        self.code = code


# N
class NotCallableError(MasonError):
    pass


# R
class ReturnException(MasonError):
    pass


# U
class UnknownExtensionError(MasonError):
    def __init__(self, extension: str = ''):
        super().__init__('Unknown file type: {}'.format(extension))
        self.extension = extension
