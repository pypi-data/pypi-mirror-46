class PyCharaException(Exception):
    pass


class LoginFailureException(PyCharaException):
    pass


class LoginRequireException(PyCharaException):
    pass


class HTTPConnectException(PyCharaException):
    pass


class HTMLParseException(PyCharaException):
    pass
