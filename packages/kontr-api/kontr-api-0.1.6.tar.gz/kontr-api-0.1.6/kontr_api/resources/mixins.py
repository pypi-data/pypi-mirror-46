def get_selector(user):
    return user if isinstance(user, str) else user.entity_id


class ClientAddsMixin(object):
    @property
    def clients(self):
        return 'users'

    def add_user(self, entity_id, user):
        return self.add_client(entity_id=entity_id, client=user, client_type='user')

    def add_users(self, entity_id, *users):
        return self.add_clients(entity_id, *users, client_type='user')

    def remove_user(self, entity_id, user):
        return self.remove_client(entity_id=entity_id, client=user, client_type='user')

    def remove_users(self, entity_id, *users):
        return self.remove_clients(entity_id, *users, client_type='user')

    def add_client(self, entity_id, client, client_type=None):
        params, url = self._get_url_for_client(entity_id, client, client_type)
        self.log.info(f"[ADD-CLIENT] {self._instance_klass.__name__} ({url}): {client}")
        response = self.rest.put(url, params=params)
        return self._make_instance(response)

    def add_clients(self, entity_id, *clients, client_type=None):
        params, url, user_selectors = self._get_url_for_clients(entity_id, client_type, clients)
        self.log.info(f"[ADD-CLIENTS] {self._instance_klass.__name__} ({url}) {user_selectors}")
        response = self.rest.put(url, {'add': user_selectors}, params=params)
        return self._make_instance(response)

    def remove_client(self, entity_id, client, client_type=None):
        params, url = self._get_url_for_client(entity_id, client, client_type)
        self.log.info(f"[DEL-CLIENT] {self._instance_klass.__name__} ({url}): {client}")
        self.rest.delete(url, params=params)

    def remove_clients(self, entity_id, *clients, client_type=None):
        params, url, user_selectors = self._get_url_for_clients(entity_id, client_type, clients)
        self.log.info(f"[DEL-CLIENTS] {self._instance_klass.__name__} ({url}): {user_selectors}")
        response = self.rest.post(url, {'remove': user_selectors}, params=params)
        return self._make_instance(response)

    def _get_url_for_clients(self, entity_id, client_type, clients):
        user_selectors = [get_selector(user) for user in clients]
        params = {} if client_type is None else dict(type=client_type)
        url = f"{self.url}/{entity_id}/{self.clients}"
        return params, url, user_selectors

    def _get_url_for_client(self, entity_id, client, client_type):
        user_selector = get_selector(client)
        params = {} if client_type is None else dict(type=client_type)
        url = f"{self.url}/{entity_id}/{self.clients}/{user_selector}"
        return params, url


class ClientAddMixin(object):
    def add_client(self, user, client_type=None):
        return self.client.add_client(self.entity_id, user, client_type=client_type)

    def add_clients(self, *users, client_type=None):
        return self.client.add_clients(self.entity_id, *users, client_type=client_type)

    def remove_client(self, user, client_type=None):
        return self.client.remove_client(self.entity_id, user, client_type=client_type)

    def remove_clients(self, *users, client_type=None):
        return self.client.remove_client(self.entity_id, *users, client_type=client_type)

    def add_user(self, user):
        return self.client.add_user(self.entity_id, user)

    def add_users(self, *users):
        return self.client.add_users(self.entity_id, *users)

    def remove_user(self, user):
        return self.client.remove_client(self.entity_id, user)

    def remove_users(self, *users):
        return self.client.remove_client(self.entity_id, *users)


class ProjectAddsMixin(object):
    def add_project(self, entity_id, project):
        user_selector = get_selector(project)
        url = f"{self.url}/{entity_id}/projects/{user_selector}"
        self.log.info(f"[ADD-PROJECT] {self._instance_klass.__name__} ({url}): {project}")
        response = self.rest.put(url)
        return self._make_instance(response)

    def add_projects(self, entity_id, *projects):
        projects_selectors = [get_selector(user) for user in projects]
        url = f"{self.url}/{entity_id}/projects/"
        self.log.info(
            f"[ADD-PROJECTS] {self._instance_klass.__name__} ({url}) {projects_selectors}")
        response = self.rest.put(url, {'add': projects_selectors})
        return self._make_instance(response)

    def remove_project(self, entity_id, projects):
        user_selector = get_selector(projects)
        url = f"{self.url}/{entity_id}/projects/{user_selector}"
        self.log.info(f"[DEL-PROJECT] {self._instance_klass.__name__} ({url}): {projects}")
        self.rest.delete(url)

    def remove_projects(self, entity_id, *projects):
        projects_selectors = [get_selector(user) for user in projects]
        url = f"{self.url}/{entity_id}/projects/"
        self.log.info(
            f"[DEL-PROJECT] {self._instance_klass.__name__} ({url}): {projects_selectors}")
        response = self.rest.post(url, {'remove': projects_selectors})
        return self._make_instance(response)


class ProjectAddMixin(object):
    def add_project(self, project):
        return self.client.add_project(self.entity_id, project)

    def add_projects(self, *projects):
        return self.client.add_projects(self.entity_id, *projects)

    def remove_project(self, project):
        return self.client.remove_project(self.entity_id, project)

    def remove_projects(self, *projects):
        return self.client.remove_projects(self.entity_id, *projects)
