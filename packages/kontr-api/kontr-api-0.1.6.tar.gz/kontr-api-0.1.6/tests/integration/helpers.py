import datetime
import logging
import random
from datetime import timedelta
from pathlib import Path
from secrets import token_urlsafe

from kontr_api import KontrClient
from kontr_api.resources import Course, Group, Project, Role, Secret, Submission, User, Worker

log = logging.getLogger(__name__)

TESTS_DIR: Path = Path(__file__).parent.parent
RESOURCES: Path = TESTS_DIR / 'resources'


def current_time() -> datetime:
    return datetime.datetime.now()


def current_delta(*args, negative=False, **kwargs):
    time_d = current_time()
    delta = timedelta(*args, **kwargs)
    if negative:
        time_d -= delta
    else:
        time_d += delta
    return time_d.isoformat()


def unique_name(name: str):
    urlsafe = token_urlsafe(5).replace('_', '')
    return (name + '-' + urlsafe).lower()


PERM_TEACHER = dict(
    view_course_full=True,
    update_course=True,
    handle_notes_access_token=False,
    write_groups=True,
    write_projects=True,
    create_submissions_other=True,
    create_submissions=True,
    resubmit_submissions=True,
    evaluate_submissions=True,
    write_reviews_all=True,
    read_submissions_groups=True,
    read_submissions_all=True
)

PERM_STUDENT = dict(
    view_course_limited=True,
    create_submissions=True,
    read_submissions_own=True,
    write_reviews_own=True
)

PERM_OWNER = dict(
    view_course_full=True,
    update_course=True,
    handle_notes_access_token=True,
    write_roles=True,
    write_groups=True,
    write_projects=True,
    resubmit_submissions=True,
    evaluate_submissions=True,
    read_submissions_all=True,
    read_all_submission_files=True,
    write_reviews_all=True
)

PERM_WORKER = dict(
    view_course_full=True,
    resubmit_submissions=True,
    evaluate_submissions=True,
    read_submissions_all=True,
    read_all_submission_files=True,
    write_reviews_all=True,
    create_submissions=True,
)

PERMISSION_TYPES = dict(
    teacher=PERM_TEACHER,
    student=PERM_STUDENT,
    owner=PERM_OWNER,
    worker=PERM_WORKER,
)


class EntitiesCreator(object):
    def __init__(self, client: KontrClient):
        self.client = client
        self.entities_stack = []

    @classmethod
    def get_user_config(cls, **kwargs) -> dict:
        uname = unique_name('test-user')
        config = dict(username=uname,
                      email=f"{uname}@example.com",
                      name='Test User',
                      uco=random.randint(1000, 100000))

        config.update(kwargs)
        return config

    def get_worker_config(self, **kwargs) -> dict:
        uname = unique_name('test-worker')
        config = dict(name=uname,
                      url=f"http://localhost:8080",
                      tags="docker gcc")

        config.update(kwargs)
        return config

    def get_secret_config(self, **kwargs) -> dict:
        uname = unique_name('test-secret')
        config = dict(name=uname)
        config.update(kwargs)
        return config

    def get_course_config(self, **kwargs) -> dict:
        uname = unique_name('test-course')
        config = dict(name=uname.capitalize(),
                      codename=uname,
                      description=f'Created Course: {uname}')

        config.update(kwargs)
        return config

    def get_project_config_config(self, **kwargs) -> dict:
        config = dict(
            test_files_source="https://gitlab.fi.muni.cz/grp-kontr2/testing/hello-test-files.git",
            file_whitelist="**/main.c",
            submission_parameters="{\"type\":\"text\"}",
            submissions_allowed_from=current_delta(days=10, negative=True),
            submissions_allowed_to=current_delta(days=360),
            archive_from=current_delta(days=3000)
        )
        config.update(kwargs)
        return config

    def get_project_config(self, **kwargs) -> dict:
        uname = unique_name('test-project')
        config = dict(name=uname.capitalize(),
                      codename=uname,
                      assignment_url='https://cecko.eu',
                      description=f"Created Project: {uname}")
        config.update(kwargs)
        return config

    def get_role_config(self, **kwargs) -> dict:
        uname = unique_name('test-role')
        config = dict(name=uname.capitalize(),
                      codename=uname,
                      description=f"Created Role: {uname}")
        config.update(kwargs)
        return config

    def get_permissions_config(self, **kwargs):
        config = dict(view_course_limited=True,
                      view_course_full=False,
                      update_course=True,
                      write_roles=False)
        config.update(kwargs)
        return config

    def get_group_config(self, **kwargs) -> dict:
        uname = unique_name('test-group')
        config = dict(name=uname.capitalize(),
                      codename=uname,
                      description=f"Created Group: {uname}")
        config.update(kwargs)
        return config

    def get_submission_config(self, **kwargs) -> dict:
        config = dict(
            file_params=dict(
                source=dict(
                    type='git',
                    url='https://gitlab.fi.muni.cz/grp-kontr2/testing/test-repo.git'
                )
            )
        )
        config.update(kwargs)
        return config

    def create_user(self, **kwargs) -> User:
        return self.create_any('user', self.client.users.create, **kwargs)

    def create_course(self, **kwargs) -> Course:
        return self.create_any('course', self.client.courses.create, **kwargs)

    def create_worker(self, **kwargs) -> Worker:
        return self.create_any('worker', self.client.workers.create, **kwargs)

    def create_secret(self, client=None, **kwargs) -> Secret:
        return self.create_any('secret', client.secrets.create, **kwargs)

    def create_project(self, course=None, **kwargs) -> Project:
        course = course or self.create_course()
        return self.create_any('project', course.projects.create, **kwargs)

    def create_role(self, course=None, perm_type=None, **kwargs) -> Role:
        course = course or self.create_course()
        role: Role = self.create_any('role', course.roles.create, **kwargs)
        perms = PERMISSION_TYPES.get(perm_type or 'student', PERM_STUDENT)
        role.permissions.update(config=perms)
        return role

    def create_group(self, course=None, **kwargs) -> Group:
        course = course or self.create_course()
        return self.create_any('group', course.groups.create, **kwargs)

    def create_submission(self, project=None, **kwargs) -> Submission:
        project = project or self.create_project()
        return self.create_any('submission', project.submissions.create,
                               delete=False, **kwargs)

    def create_any(self, resource=None, create_method=None,
                   delete=True, **kwargs):
        conf_method = getattr(self, f"get_{resource}_config")
        config = conf_method(**kwargs)
        log.info(f"[DATA] Create {resource}: {config}")
        entity = create_method(config=config)
        if delete:
            self.entities_stack.append(entity)
        return entity

    def clean_stack(self):
        reverse = self.entities_stack[::-1]
        for entity in reverse:
            log.debug(f"[CLEAN] Cleaning entity: {entity}")
            entity.delete()


def assert_params(expected, entity, params=None):
    assert entity['id'] is not None
    params = params or expected.keys()
    for param in params:
        message = f"Param: {param}: {expected[param]} == {entity[param]}"
        assert expected[param] == entity[param], message


def assert_not_in_collection(entity_testing, user_entity, collection):
    collection_ids = [item['id'] for item in entity_testing[collection]]
    assert user_entity.entity_id not in collection_ids


def assert_in_collection(entity_testing, user_entity, collection):
    collection_ids = [item['id'] for item in entity_testing[collection]]
    assert user_entity.entity_id in collection_ids
