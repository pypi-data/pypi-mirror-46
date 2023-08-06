import pytest

from kontr_api.resources import Secret, User, Worker
from tests.integration.helpers import EntitiesCreator


@pytest.fixture()
def worker_testing(ent_creator: EntitiesCreator) -> Worker:
    worker = ent_creator.create_worker()
    return worker


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator, worker_testing) -> Secret:
    secret = ent_creator.create_secret(worker_testing)
    return secret


@pytest.fixture()
def entity_client(worker_testing):
    return worker_testing.secrets


def test_secret_has_been_created(entity_client, ent_creator):
    secret_config = ent_creator.get_secret_config()
    created = entity_client.create(secret_config)
    assert created['id'] is not None
    assert created['value'] is not None
    ent_creator.entities_stack.append(created)


def test_secret_should_be_listed(entity_client, entity_testing: User):
    secrets_list = entity_client.list()
    assert len(secrets_list) > 0
    assert entity_testing in secrets_list


def test_secret_should_be_deleted(entity_client, entity_testing: User):
    assert entity_testing in entity_client.list()
    entity_testing.delete()
    assert entity_testing not in entity_client.list()
