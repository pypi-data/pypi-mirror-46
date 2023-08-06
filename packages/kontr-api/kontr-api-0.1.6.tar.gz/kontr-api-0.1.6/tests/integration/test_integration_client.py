import pytest

from kontr_api import resources
from kontr_api.resources import User


@pytest.fixture()
def entity_client(client):
    return client.clients


def test_clients_me_should_be_current_user(current_user: User, entity_client: resources.Clients):
    me = entity_client.me()
    assert me['codename'] == current_user['codename']
    assert me['type'] == current_user['type']
    assert me['id'] == current_user['id']
    assert me['name'] == current_user['name']
