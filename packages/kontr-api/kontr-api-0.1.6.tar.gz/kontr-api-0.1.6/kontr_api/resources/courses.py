from kontr_api.resources.default import Default, Defaults


class Courses(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Course)

    def read_is_api_token(self, eid, **kwargs):
        url = self._get_resource_url(eid) + '/notes_access_token'
        self.log.debug(f"[READ] Course IS MU API access token ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_instance(response, instance_klass=dict)

    def update_is_api_token(self, eid, token=None, **kwargs):
        url = self._get_resource_url(eid) + '/notes_access_token'
        self.log.info(f"[UPDATE] Course IS MU API access token ({url}): {token}")
        body = dict(token=token)
        response = self.rest.put(url, json=body, **kwargs)
        return self._make_instance(response, instance_klass=dict)


class Course(Default):
    @property
    def projects(self):
        from kontr_api.resources.projects import Projects
        return Projects(self)

    @property
    def roles(self):
        from kontr_api.resources.roles import Roles
        return Roles(self)

    @property
    def groups(self):
        from kontr_api.resources.groups import Groups
        return Groups(self)

    def read_is_api_token(self, **kwargs):
        return self.client.read_is_api_token(self.entity_id, **kwargs)

    def update_is_api_token(self, token=None, **kwargs):
        return self.client.update_is_api_token(self.entity_id, token=token, **kwargs)
