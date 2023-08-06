import datetime
import logging
from typing import Optional

import requests

log = logging.getLogger(__name__)


class Tokens(object):
    def __init__(self, auth: 'AuthBase', access_token: str = None, refresh_token: str = None):
        """Creates tokens instance
        Args:
            auth(AuthBase): Auth base instance
            access_token(str): Access token
            refresh_token(str): Refresh token
        """
        self._auth = auth
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def auth(self) -> 'AuthBase':
        """Gets auth base instance
        Returns(AuthBase): Auth base instance
        """
        return self._auth

    @property
    def access(self) -> str:
        """Gets access token instance
        Returns(str): Access token
        """
        if self._access_token is None:
            self._get_access_token()
        return self._access_token

    @property
    def refresh(self) -> str:
        """Gets refresh token
        Returns(str): Refresh token
        """
        if self._refresh_token is None:
            self._get_refresh_token()
        return self._refresh_token

    def clear_tokens(self):
        """Clears all the tokens
        """
        log.debug("[TOKENS] Clearing tokens")
        self.clear_access_token()
        self._refresh_token = None

    def clear_access_token(self):
        """Clear all access token
        """
        log.debug("[TOKENS] Clearing access token")
        self._access_token = None

    def check_tokens(self) -> bool:
        """Checks tokens
        Returns(bool): True if all tokens are valid
        """
        ok = True
        ok &= self.check_access_token()
        ok &= self.check_refresh_token()
        return ok

    def _get_refresh_token(self):
        """Gets refresh token
        """
        login = self.auth.login()
        if login is not None:
            self._refresh_token = login['refresh_token']
            self._access_token = login['access_token']

    def _get_access_token(self):
        """Gets access token
        """
        if not self._refresh_token:
            self._get_refresh_token()
            return
        refresh = self.auth.refresh()
        if refresh is not None:
            self._access_token = refresh['access_token']

    def check_access_token(self) -> bool:
        """Checks access token
        Returns(bool): True if access token is valid

        """
        if not _validate_token(self.access):
            self.clear_access_token()
            return False
        return True

    def check_refresh_token(self) -> bool:
        """Checks refresh token
        Returns(bool): True of refresh token is true
        """
        if not _validate_token(self.refresh):
            self.clear_tokens()
            return False
        return True


class AuthBase(object):
    def __init__(self, url, access_token=None, refresh_token=None, **credentials):
        """Creates auth base instance
        Args:
            url(str): Url to kontr backend
            access_token(str): access token
            refresh_token:(str)  Refresh token
            **credentials: another credentials (username, password, secret)
        """
        self.url = url
        self._credentials = _build_credentials(**credentials)
        self._tokens = Tokens(self, access_token=access_token, refresh_token=refresh_token)

    @property
    def tokens(self) -> Tokens:
        """Gets instance of the tokens holder
        Returns(Tokens): Tokens holder instance
        """
        return self._tokens

    @property
    def login_url(self) -> str:
        """Gets login url
        Returns(str): Login url

        """
        return f"{self.url}/auth/login"

    @property
    def refresh_url(self):
        """Gets refresh url
        Returns(str): Refresh url
        """
        return f"{self.url}/auth/refresh"

    def login(self) -> Optional[dict]:
        """Log in to the portal using credentials
        Returns(Optional[dict]): Tokens - access and refresh token
        """
        if self._credentials is None:
            return None
        log.info(f"[LOGIN] Login {self.login_url}")
        response = requests.post(self.login_url, json=self._credentials)
        json_response = response.json()
        log.debug(f"[LOGIN] Response: {json_response}")
        return json_response

    def refresh(self) -> Optional[dict]:
        """Gets access token using refresh token
        Returns(Optional[dict]): Access token
        """
        if self.tokens.refresh is None:
            return None
        headers = {'Authorization': 'Bearer ' + self.tokens.refresh}
        log.info(f"[LOGIN] Refresh {self.refresh_url}")
        response = requests.post(self.refresh_url, headers=headers)
        json_response = response.json()
        log.debug(f"[LOGIN] Refresh Response: {json_response}")
        return json_response

    @property
    def access_header(self) -> dict:
        """Creates access header
        Returns(dict): Created authorization header
        """
        return {'Authorization': 'Bearer ' + self.tokens.access}


def _build_credentials(username: str = None, password: str = None, identifier: str = None,
                       secret: str = None):
    login_type = 'secret' if secret else 'username_password'
    identifier = identifier or username
    secret = secret or password
    return dict(type=login_type, identifier=identifier, secret=secret)


def _validate_token(token: str) -> bool:
    """Validates token
    Args:
        token(str): Token

    Returns(bool): true if token is valid

    """
    import jwt
    decoded = jwt.decode(token, verify=False)
    expiration_stamp = decoded['exp']
    exp_date = datetime.datetime.fromtimestamp(int(expiration_stamp))
    present = datetime.datetime.now()
    log.debug(f"[TOKEN] Comparing: {exp_date} > {present}: { exp_date > present } ")
    return exp_date > present
