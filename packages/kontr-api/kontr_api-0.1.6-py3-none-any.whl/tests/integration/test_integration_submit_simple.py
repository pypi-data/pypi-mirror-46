import logging
import time

import pytest

from kontr_api.resources import Submission
from tests.integration.helpers import RESOURCES

log = logging.getLogger(__name__)


@pytest.fixture()
def new_submission(ent_creator, current_user, active_project,
                   role_testing, group_testing, worker) -> Submission:
    role_testing.add_client(current_user)
    group_testing.add_client(current_user)
    submission = ent_creator.create_submission(project=active_project)
    yield submission
    submission.cancel()


def wait_for_status(submission: Submission, expected=None):
    repeat = 10
    if not expected:
        expected = ['READY', 'ABORTED']
    state = None
    while state not in expected:
        log.debug(f"[WAIT] Waiting for submission status {state} to be one of {expected}")
        state = submission['state']
        time.sleep(2)
        repeat -= 1
        submission.read()
        if not repeat:
            return False
    return True


def assert_subm_file_content(submission: Submission, path: str):
    assert submission.sources.content(path)


def assert_result_file_content(submission: Submission, path: str):
    assert submission.results.content(path)


def upload_result(new_submission):
    result_path = RESOURCES / 'result.zip'
    new_submission.results.upload(result_path)


def assert_subm_file_tree(new_submission: Submission):
    assert new_submission.sources.tree()


def test_create_new_submission(new_submission, current_user, project_testing):
    assert new_submission['id'] is not None
    assert new_submission['user']['id'] == current_user.entity_id
    assert new_submission['project']['id'] == project_testing.entity_id

    assert wait_for_status(new_submission)
    assert new_submission['state'] in ['READY', 'ABORTED']
    assert_subm_file_content(new_submission, 'hw01/main.c')
    assert_subm_file_content(new_submission, 'hw02/src/main.c')
    assert_subm_file_tree(new_submission)

    upload_result(new_submission)

    wait_for_status(new_submission, expected='FINISHED')

    assert_result_file_content(new_submission, 'tests_result.json')
    assert_result_file_content(new_submission, 'test_result_reduced.json')
    stats = new_submission.stats()
    assert stats
