from requests import Response


class KontrApiError(Exception):
    pass


class RequestHasFailedError(Exception):
    def __init__(self, response: Response):
        message = f"Request failed [{response.status_code}]: {response.raw}"
        self.response = response
        super(RequestHasFailedError, self).__init__(message)
