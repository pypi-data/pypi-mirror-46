import logging
from pathlib import Path

import requests
from requests import Response

from kontr_api import errors
from kontr_api.auth import AuthBase
from kontr_api.errors import RequestHasFailedError

log = logging.getLogger(__name__)


class KontrRestClient(object):
    def __init__(self, kontr_client):
        self.kontr_client = kontr_client

    @property
    def url(self):
        return self.kontr_client.url

    @property
    def auth(self) -> AuthBase:
        """ Gets an instance of he auth base
        Returns(AuthBase): instance of the auth base
        """
        return self.kontr_client.auth

    def get(self, *args, **kwargs):
        """Makes get request on the endpoint
        Args:
            *args:
            **kwargs:
        Returns(dict): Serialized JSON response
        """
        return self.request('get', *args, **kwargs)

    def head(self, *args, **kwargs):
        """Makes head request on the endpoint
        Args:
            *args: Arguments for the rest client
            **kwargs: Keyword args for the rest client
        Returns(dict): Serialized JSON response
        """
        return self.request('head', *args, **kwargs)

    def options(self, *args, **kwargs):
        """Makes options request on the endpoint
        Args:
            *args: Arguments for the rest client
            **kwargs: Keyword args for the rest client
        Returns(dict): Serialized JSON response
        """
        return self.request('options', *args, **kwargs)

    def post(self, *args, **kwargs):
        """Makes post request on the endpoint
         Args:
             *args:
             **kwargs:
         Returns(dict): Serialized JSON response
         """
        return self.request('post', *args, **kwargs)

    def put(self, *args, **kwargs):
        """Makes put request on the endpoint
         Args:
             *args:
             **kwargs:
         Returns(dict): Serialized JSON response
         """
        return self.request('put', *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Makes delete request on the endpoint
         Args:
             *args:
             **kwargs:
         Returns(dict): Serialized JSON response
         """
        return self.request('delete', *args, **kwargs)

    def request(self, method: str, path: str, headers: dict = None, **kwargs) -> Response:
        headers = headers or {}
        self.auth.tokens.check_tokens()
        head = {**headers, **self.auth.access_header}
        response = requests.request(method, path, headers=head, **kwargs)
        log.debug(f"[RESP] Response({response.status_code}): {response.content}")
        return self.__check_response(response)

    def __check_response(self, response: Response):
        if not response.ok:
            return self.__handle_failed(response)
        return response

    def __handle_failed(self, response: Response):
        log.warning(f"[RESP] Warning ({response.status_code}): {response.content}")
        if self.kontr_client.throw:
            raise RequestHasFailedError(response)
        return None

    def download_file(self, url, path: Path):
        # NOTE the stream=True parameter
        path = Path(path)
        response = self.get(url, stream=True)
        if response is None:
            raise errors.KontrApiError("File does not exists!")
        with path.open('wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush() commented by recommendation from J.F.Sebastian
        return path

    def upload_file(self, url, path: Path):
        path = Path(path)
        files = {'file': path.open('rb')}
        return self.post(url, files=files)
