import pytest

from kontr_api.resources import Course, Project
from tests.integration.helpers import EntitiesCreator, assert_params


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Project:
    entity = ent_creator.create_project(course=course_testing)
    return entity


@pytest.fixture()
def entity_client(course_testing: Course):
    return course_testing.projects


def test_project_has_been_created(entity_client, ent_creator: EntitiesCreator):
    entity_config = ent_creator.get_project_config()
    created = entity_client.create(entity_config)
    assert_params(expected=entity_config, entity=created, params=['name', 'description'])
    ent_creator.entities_stack.append(created)


def test_project_should_be_listed(entity_client, entity_testing):
    entities = entity_client.list()
    assert len(entities) > 0
    assert entity_testing in entities


def test_project_should_be_updated(entity_client, entity_testing):
    param = 'description'
    old_name = entity_testing[param]
    new_name = old_name + " Updated"
    entity_testing[param] = new_name
    entity_testing.update()
    assert entity_testing[param] == new_name


def test_project_should_be_deleted(entity_client, entity_testing):
    assert entity_testing in entity_client.list()
    entity_testing.delete()
    assert entity_testing not in entity_client.list()
