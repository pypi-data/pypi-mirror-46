import pytest

from kontr_api.resources import Course, Permissions, PermissionsObject, Role
from tests.integration.helpers import EntitiesCreator, assert_params


@pytest.fixture()
def role_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Role:
    entity = ent_creator.create_role(course=course_testing)
    return entity


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator, entity_client: Permissions) -> PermissionsObject:
    entity_client.update(ent_creator.get_permissions_config())
    entity = entity_client.read()
    return entity


@pytest.fixture()
def entity_client(role_testing: Role):
    return role_testing.permissions


def test_role_permissions_has_been_set(entity_testing, ent_creator: EntitiesCreator):
    entity_config = ent_creator.get_permissions_config()
    params = ['view_course_limited', 'view_course_full', 'update_course',
              'write_roles']
    assert_params(expected=entity_config, entity=entity_testing, params=params)


def test_project_should_be_updated(entity_client, entity_testing):
    param = 'write_roles'
    new_name = True
    entity_testing[param] = new_name
    entity_testing.update()
    assert entity_testing[param] == new_name
