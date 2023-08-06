import pytest

from kontr_api.resources import User, Worker
from tests.integration.helpers import EntitiesCreator


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator)-> Worker:
    worker = ent_creator.create_worker()
    return worker


@pytest.fixture()
def entity_client(client):
    return client.workers


def test_worker_has_been_created(entity_client, ent_creator):
    worker_config = ent_creator.get_worker_config()
    created = entity_client.create(worker_config)
    assert created['id'] is not None
    assert created['name'] == worker_config['name']
    assert created['tags'] == worker_config['tags']
    assert created['url'] == worker_config['url']
    ent_creator.entities_stack.append(created)


def test_worker_should_be_listed(entity_client, entity_testing: Worker):
    workers_list = entity_client.list()
    assert len(workers_list) > 0
    assert entity_testing in workers_list


def test_worker_should_be_updated(client, entity_testing: Worker):
    old_tags = entity_testing['tags']
    new_tags = old_tags + " valgrind"
    entity_testing['tags'] = new_tags
    entity_testing.update()
    assert entity_testing['tags'] == new_tags


def test_worker_should_be_deleted(entity_client, entity_testing: Worker):
    assert entity_testing in entity_client.list()
    entity_testing.delete()
    assert entity_testing not in entity_client.list()


