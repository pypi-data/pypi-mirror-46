import pytest

from kontr_api import KontrClient
from kontr_api.resources import User
from tests.integration.helpers import EntitiesCreator


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator) -> User:
    user = ent_creator.create_user()
    return user


@pytest.fixture()
def entity_client(client):
    return client.users


def test_user_has_been_created(entity_client, ent_creator):
    user_config = ent_creator.get_user_config()
    created = entity_client.create(user_config)
    assert created['id'] is not None
    assert created['name'] == user_config['name']
    assert created['email'] == user_config['email']
    assert created['username'] == user_config['username']
    assert created['uco'] == user_config['uco']
    ent_creator.entities_stack.append(created)


def test_user_should_be_listed(entity_client, entity_testing: User):
    users_list = entity_client.list()
    assert len(users_list) > 0
    assert entity_testing in users_list


def test_user_should_be_updated(client, entity_testing: User):
    old_uco = entity_testing['uco']
    new_uco = old_uco + 1
    entity_testing['uco'] = new_uco
    entity_testing.update()
    assert entity_testing['uco'] == new_uco


def test_user_should_be_deleted(entity_client, entity_testing: User):
    assert entity_testing in entity_client.list()
    entity_testing.delete()
    assert entity_testing not in entity_client.list()


def test_user_should_change_password(entity_client, url, entity_testing: User):
    new_password = 'TestPassword1.0'
    entity_testing.set_password(new_password)
    username = entity_testing['username']
    login = get_client(url, username, new_password)
    assert login['access_token']
    assert login['refresh_token']
    login = get_client(url, username, 'wrong_password')
    assert not login.get('access_token')
    assert not login.get('refresh_token')


def get_client(url, username, new_password):
    client = KontrClient(url=url, username=username, password=new_password)
    login = client.login()
    return login




