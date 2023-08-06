import pytest

from kontr_api.resources import Course, Project, ProjectConfig, ProjectConfigs
from tests.integration.helpers import EntitiesCreator, assert_params


@pytest.fixture()
def project_testing(ent_creator: EntitiesCreator, course_testing: Course) -> Project:
    entity = ent_creator.create_project(course=course_testing)
    return entity


@pytest.fixture()
def entity_testing(ent_creator: EntitiesCreator, entity_client: ProjectConfigs) -> ProjectConfig:
    entity_client.update(ent_creator.get_project_config_config())
    entity = entity_client.read()
    return entity


@pytest.fixture()
def entity_client(project_testing: Project):
    return project_testing.project_config


def test_project_config_has_been_set(entity_testing, ent_creator: EntitiesCreator):
    entity_config = ent_creator.get_project_config_config()
    params = ['test_files_source', 'file_whitelist', 'submission_parameters']
    assert_params(expected=entity_config, entity=entity_testing, params=params)


def test_project_should_be_updated(entity_client, entity_testing):
    param = 'submission_parameters'
    old_name = entity_testing[param]
    new_name = old_name + " Updated"
    entity_testing[param] = new_name
    entity_testing.update()
    assert entity_testing[param] == new_name

