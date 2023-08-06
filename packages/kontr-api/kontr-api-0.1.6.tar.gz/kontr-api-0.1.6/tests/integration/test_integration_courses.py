import pytest

from kontr_api.resources import Course
from tests.integration.helpers import EntitiesCreator, assert_params


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator) -> Course:
    course = ent_creator.create_course()
    yield course
    course.delete()


@pytest.fixture()
def entity_client(client):
    return client.courses


def test_course_has_been_created(entity_client, ent_creator: EntitiesCreator):
    course_config = ent_creator.get_course_config()
    created = entity_client.create(course_config)
    assert created['id'] is not None
    assert created['name'] == course_config['name']
    assert created['codename'] == course_config['codename']
    assert created['description'] == course_config['description']
    assert_params(course_config, created)
    ent_creator.entities_stack.append(created)


def test_course_should_be_listed(entity_client, entity_testing):
    entities = entity_client.list()
    assert len(entities) > 0
    assert entity_testing in entities


def test_course_should_be_updated(entity_client, entity_testing):
    param = 'name'
    old_name = entity_testing[param]
    new_name = old_name + " Updated"
    entity_testing[param] = new_name
    entity_testing.update()
    assert entity_testing[param] == new_name


def test_course_should_be_deleted(entity_client, entity_testing: Course):
    assert entity_testing in entity_client.list()
    entity_testing.delete()
    assert entity_testing not in entity_client.list()


def test_course_set_access_token(entity_client, entity_testing: Course):
    entity_testing.update_is_api_token(token='test_token')
    token = entity_testing.read_is_api_token()
    assert token == 'test_token'
