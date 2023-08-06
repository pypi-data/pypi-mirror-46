import logging

from kontr_api import log_config, resources
from kontr_api.auth import AuthBase
from kontr_api.rest_client import KontrRestClient

log = logging.getLogger(__name__)


class KontrClient(object):
    def __init__(self, url: str, api_version: str = 'v1.0',
                 secret: str = None, identifier: str = None,
                 username: str = None, password: str = None,
                 access_token: str = None, refresh_token: str = None,
                 enable_logging: bool = False, throw: bool = False):
        """Initializes the Kontr Client
        Args:
            url(str): Url of the Kontr Portal
            api_version(str): API Version - default: 'v1.0'
            secret(str): Secret
            identifier(str): Identifier
            username(str): Username
            password(str): Password
            access_token(str): Access token - if provided will be used this one
            refresh_token(str): Refresh token - if provided will be used this one
        """
        if enable_logging:
            log_config.load_config()
        self._api_url = url + '/api/' + api_version
        self._portal_url = url
        self._auth = AuthBase(self.url, secret=secret, identifier=identifier,
                              username=username, password=password,
                              access_token=access_token, refresh_token=refresh_token)
        self._rest = KontrRestClient(self)
        self._throw = throw
        log.debug(f"[INIT] Kontr client: {self.url}")

    @property
    def throw(self) -> bool:
        """Whether to throw an exception at failure
        Returns(bool): Whether to throw exception at failure
        """
        return self._throw

    @property
    def rest(self) -> KontrRestClient:
        """Gets rest API client
        Returns(KontrRestClient): Kontr Rest client instance
        """
        return self._rest

    @property
    def kontr_client(self) -> 'KontrClient':
        """Gets Kontr client instance
        Returns(KontrClient): Kontr Client instance
        """
        return self

    @property
    def portal_url(self) -> str:
        """Returns portal url
        Returns(str): Portal url
        """
        return self._portal_url

    @property
    def url(self) -> str:
        """Gets REST API url
        Returns(str): Rest API url with version
        """
        return self._api_url

    @property
    def auth(self) -> AuthBase:
        """Gets Auth base object
        Returns(AuthBase): Auth base object
        """
        return self._auth

    @property
    def users(self) -> resources.Users:
        """Returns Users collection client
        Returns(resources.Users): Users client instance
        """
        return resources.Users(self)

    @property
    def clients(self) -> resources.Clients:
        """Returns Users collection client
        Returns(resources.Users): Users client instance
        """
        return resources.Clients(self)

    @property
    def courses(self) -> resources.Courses:
        """Gets instance of Courses collection
        Returns(resources.Courses): Courses collection instance
        """
        return resources.Courses(self)

    @property
    def submissions(self) -> resources.Submissions:
        """Gets instance of the Submissions instance
        Returns(resources.Submissions): Submissions collection

        """
        return resources.Submissions(self)

    @property
    def workers(self) -> resources.Workers:
        """Gets an instance of the Worker collection
        Returns(resources.Workers): Workers collection instance

        """
        return resources.Workers(self)

    @property
    def definitions(self) -> resources.Definitions:
        """Gets an instance of the definition management
        Returns(resources.Definitions): Definitions

        """
        return resources.Definitions(self)

    @property
    def management(self) -> resources.Management:
        """Gets an instance of the kontr management functions
        Returns(resources.Management): Management functions

        """
        return resources.Management(self)

    @property
    def analytics(self) -> resources.Analytics:
        """Gets an instance of the analytics functions
        Returns(resources.Management): Analytics functions

        """
        return resources.Analytics(self)

    def login(self) -> dict:
        """Login to the kontr portal backend
        Returns:

        """
        return self.auth.login()
