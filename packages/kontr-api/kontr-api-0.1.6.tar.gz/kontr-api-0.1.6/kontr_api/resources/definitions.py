from typing import Dict

import yaml

from kontr_api.resources import Course, Group, Project, Role
from kontr_api.resources.default import Defaults


class Definitions(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=None)
        self._url = self.parent.url + f"/definition"

    def sync_course(self, schema: Dict, **kwargs):
        url = self.url + "/courses"
        self.log.info(f"[SYNC] Course ({url})")
        data = yaml.safe_dump(schema)
        response = self.rest.post(url, data=data, **kwargs)
        return self._make_instance(response, instance_klass=Course)

    def sync_project(self, course_id: str, schema: Dict, **kwargs):
        url = self.url + f"/courses/{course_id}/projects"
        self.log.info(f"[SYNC] Project ({url})")
        data = yaml.safe_dump(schema)
        response = self.rest.post(url, data=data, **kwargs)
        return self._make_instance(response, instance_klass=Project)

    def sync_role(self, course_id: str, schema: Dict, **kwargs):
        url = self.url + f"/courses/{course_id}/roles"
        self.log.info(f"[SYNC] Role ({url})")
        data = yaml.safe_dump(schema)
        response = self.rest.post(url, data=data, **kwargs)
        return self._make_instance(response, instance_klass=Role)

    def sync_group(self, course_id: str, schema: Dict, **kwargs):
        url = self.url + f"/courses/{course_id}/groups"
        self.log.info(f"[SYNC] Group ({url})")
        data = yaml.safe_dump(schema)
        response = self.rest.post(url, data=data, **kwargs)
        return self._make_instance(response, instance_klass=Group)

    def dump_course(self, course_id: str, **kwargs):
        url = self.url + f"/courses/{course_id}"
        self.log.info(f"[DUMP] Course ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_instance(response, raw=True)

    def dump_project(self, course_id: str, project_id: str, **kwargs):
        url = self.url + f"/courses/{course_id}/projects/{project_id}"
        self.log.info(f"[DUMP] Project ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_instance(response, raw=True)

    def dump_role(self, course_id: str, role_id: str, **kwargs):
        url = self.url + f"/courses/{course_id}/roles/{role_id}"
        self.log.info(f"[DUMP] Project ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_instance(response, raw=True)

    def dump_group(self, course_id: str, group_id: str, **kwargs):
        url = self.url + f"/courses/{course_id}/groups/{group_id}"
        self.log.info(f"[DUMP] Group ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_instance(response, raw=True)
