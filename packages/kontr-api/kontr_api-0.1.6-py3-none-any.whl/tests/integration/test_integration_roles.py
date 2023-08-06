import pytest

from kontr_api.resources import Course, User, Role, Roles
from tests.integration.helpers import EntitiesCreator, assert_params, assert_in_collection, \
    assert_not_in_collection


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Role:
    return ent_creator.create_role(course=course_testing)


@pytest.fixture()
def entity_client(course_testing: Course) -> Roles:
    return course_testing.roles


def test_roles_has_been_created(entity_client, ent_creator: EntitiesCreator):
    entity_config = ent_creator.get_role_config()
    created = entity_client.create(entity_config)
    assert_params(expected=entity_config, entity=created, params=['name', 'description'])
    ent_creator.entities_stack.append(created)


def test_roles_should_be_listed(entity_client, entity_testing):
    entities = entity_client.list()
    assert len(entities) > 0
    assert entity_testing in entities


def test_roles_should_be_updated(entity_client, entity_testing):
    param = 'description'
    old_name = entity_testing[param]
    new_name = old_name + " Updated"
    entity_testing[param] = new_name
    entity_testing.update()
    assert entity_testing[param] == new_name


def test_roles_should_be_deleted(entity_client, entity_testing):
    assert entity_testing in entity_client.list()
    entity_testing.delete()
    assert entity_testing not in entity_client.list()


@pytest.fixture()
def user_entity(ent_creator: EntitiesCreator) -> User:
    return ent_creator.create_user()


def test_roles_add_user(entity_client, entity_testing, user_entity):
    assert_not_in_collection(entity_testing, user_entity, 'clients')
    entity_testing.add_user(user_entity)
    entity_testing.read()
    assert_in_collection(entity_testing, user_entity, 'clients')


def test_roles_del_user(entity_client, entity_testing, user_entity):
    entity_testing.add_user(user_entity)
    entity_testing.read()
    assert_in_collection(entity_testing, user_entity, 'clients')
    entity_testing.remove_user(user_entity)
    entity_testing.read()
    assert_not_in_collection(entity_testing, user_entity, 'clients')
