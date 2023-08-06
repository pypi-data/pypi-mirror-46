import os

import pytest

from kontr_api import KontrClient
from kontr_api.resources import Course, Project, Role, Group, User
from tests.integration.helpers import EntitiesCreator


@pytest.fixture()
def url():
    return os.getenv('TEST_PORTAL_URL', 'http://localhost:8000')


@pytest.fixture()
def user_name():
    return os.getenv('TEST_PORTAL_USERNAME', 'admin')


@pytest.fixture()
def user_password():
    return os.getenv('TEST_PORTAL_USERNAME', '789789')


@pytest.fixture()
def worker_name():
    return os.getenv('TEST_PORTAL_WORKER', 'executor')


@pytest.fixture()
def client(url, user_name, user_password):
    return KontrClient(url=url, username=user_name, password=user_password)


@pytest.fixture()
def current_user(client, user_name) -> User:
    return client.users[user_name]


@pytest.fixture()
def worker(client, worker_name):
    return client.workers[worker_name]


@pytest.fixture()
def ent_creator(client):
    creator = EntitiesCreator(client)
    yield creator
    creator.clean_stack()


@pytest.fixture()
def course_testing(ent_creator: EntitiesCreator) -> Course:
    entity = ent_creator.create_course()
    return entity


@pytest.fixture()
def project_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Project:
    return ent_creator.create_project(course=course_testing)


@pytest.fixture()
def active_project(ent_creator: EntitiesCreator, project_testing: Project) -> Project:
    config = ent_creator.get_project_config_config()
    instance = project_testing.project_config.update(config)
    project_testing.read()
    return project_testing


@pytest.fixture()
def role_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Role:
    return ent_creator.create_role(course=course_testing)


@pytest.fixture()
def group_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Group:
    return ent_creator.create_group(course=course_testing)
