import pytest

from kontr_api import resources


@pytest.fixture()
def entity_client(client) -> resources.Analytics:
    return client.analytics


def test_mgmt_logs_file_should_be_available(entity_client: resources.Analytics):
    fc = entity_client.submissions()
    assert fc is not None
    assert isinstance(fc, list)

    submission = fc[0]
    assert isinstance(submission, dict)
    assert submission['user_hash'] is not None
