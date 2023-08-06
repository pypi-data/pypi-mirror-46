import pytest

from kontr_api import resources
from kontr_api.resources import User, Management


@pytest.fixture()
def entity_client(client) -> Management:
    return client.management


def test_management_status_should_be_working(entity_client: resources.Management):
    assert entity_client.status() is not None


def test_mgmt_logs_tree_should_be_dict(entity_client: resources.Management):
    tree = entity_client.logs_tree()
    assert tree is not None
    assert isinstance(tree, dict)


def test_mgmt_logs_file_should_be_available(entity_client: resources.Management):
    fc = entity_client.logs_file(path='portal.log')
    assert fc is not None

