class RestException(Exception):
    def __init__(self, message=None, status_code=None) -> None:
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class BadRequest(RestException):
    def __init__(self, message=None) -> None:
        super().__init__(message, 400)


class InternalServerError(RestException):
    def __init__(self, message=None) -> None:
        super().__init__(message, 500)


class MethodNotAllowed(RestException):
    def __init__(self, message=None) -> None:
        super().__init__(message, 405)
