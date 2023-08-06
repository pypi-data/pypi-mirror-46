import pytest
import yaml

from kontr_api.resources import Course, Definitions


@pytest.fixture()
def entity_client(client) -> Definitions:
    return client.definitions


@pytest.fixture()
def course(current_user, active_project, role_testing, group_testing) -> Course:
    return active_project.course


def test_dump_course_schema(course, entity_client: Definitions):
    dump = entity_client.dump_course(course_id=course['codename'])
    yaml_dump = yaml.safe_load(dump)
    assert yaml_dump['codename'] == course['codename']
    assert yaml_dump['name'] == course['name']


def test_dump_project_schema(course, entity_client: Definitions, active_project):
    dump = entity_client.dump_project(course_id=course['codename'], project_id=active_project['id'])
    yaml_dump = yaml.safe_load(dump)
    assert yaml_dump['codename'] == active_project['codename']
    assert yaml_dump['name'] == active_project['name']


def test_dump_role_schema(course, entity_client: Definitions, role_testing):
    dump = entity_client.dump_role(course_id=course['codename'], role_id=role_testing['id'])
    yaml_dump = yaml.safe_load(dump)
    assert yaml_dump['codename'] == role_testing['codename']
    assert yaml_dump['name'] == role_testing['name']


def test_dump_group_schema(course, entity_client: Definitions, group_testing):
    dump = entity_client.dump_group(course_id=course['codename'], group_id=group_testing['id'])
    yaml_dump = yaml.safe_load(dump)
    assert yaml_dump['codename'] == group_testing['codename']
    assert yaml_dump['name'] == group_testing['name']


def test_sync_course_schema(course, entity_client: Definitions):
    dump = entity_client.dump_course(course_id=course['codename'])
    yaml_dump = yaml.safe_load(dump)
    yaml_dump['name'] = "New name"
    synced = entity_client.sync_course(yaml_dump)
    assert yaml_dump['codename'] == synced['codename']
    assert yaml_dump['name'] == synced['name']


def test_sync_project_schema(course, entity_client: Definitions, active_project):
    dump = entity_client.dump_project(course_id=course['codename'], project_id=active_project['id'])
    yaml_dump = yaml.safe_load(dump)
    yaml_dump['name'] = "New name"
    synced = entity_client.sync_project(course_id=course['codename'], schema=yaml_dump)
    assert yaml_dump['codename'] == synced['codename']
    assert yaml_dump['name'] == synced['name']


def test_sync_group_schema(course, entity_client: Definitions, group_testing):
    dump = entity_client.dump_group(course_id=course['codename'], group_id=group_testing['id'])
    yaml_dump = yaml.safe_load(dump)
    yaml_dump['name'] = "New name"
    synced = entity_client.sync_group(course_id=course['codename'], schema=yaml_dump)
    assert yaml_dump['codename'] == synced['codename']
    assert yaml_dump['name'] == synced['name']


def test_sync_role_schema(course, entity_client: Definitions, role_testing):
    dump = entity_client.dump_role(course_id=course['codename'], role_id=role_testing['id'])
    yaml_dump = yaml.safe_load(dump)
    yaml_dump['name'] = "New name"
    synced = entity_client.sync_role(course_id=course['codename'], schema=yaml_dump)
    assert yaml_dump['codename'] == synced['codename']
    assert yaml_dump['name'] == synced['name']
