import pytest

from kontr_api import KontrClient


@pytest.fixture()
def auth(client: KontrClient):
    return client.auth


@pytest.fixture()
def login(auth):
    return auth.login()


def test_auth_login(login):
    assert login is not None
    assert 'access_token' in login.keys()
    assert 'refresh_token' in login.keys()


def test_auth_refresh(auth):
    auth.login()
    auth.tokens.clear_access_token()
    response = auth.refresh()
    assert 'access_token' in response.keys()


def test_auth_clean(auth):
    auth.login()
    auth.tokens.clear_tokens()
    response = auth.refresh()
    assert 'access_token' in response.keys()
