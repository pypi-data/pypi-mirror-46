from kontr_api.resources.default import Default, Defaults


class ProjectConfigs(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=ProjectConfig)

    @property
    def url(self) -> str:
        return f"{self.parent.url}/config"


class ProjectConfig(Default):
    @property
    def project(self) -> 'Project':
        return self.parent

    def update(self, config: dict=None):
        return self.client.update(config)

    def read(self):
        return self.client.read()


class Projects(Defaults):
    def __init__(self, parent):
        """Creates instance of the projects collection
        Args:
            parent: Parent resource
        """
        super().__init__(parent, instance_klass=Project)

    def submit(self, entity_id: str, config):
        """Create new submission
        Args:
            entity_id(str): Entity id
            config(dict): Submit configuration

        Config:
            file_params(dict): File params (GIT|ZIP|SVN)
            project_params(dict): Project params

        File params:
            source(dict): Source schema
        Source:
            type(str): Submission source type: 'git'
            url(str): Repo url
            branch(str): Repo branch (default: master)
            checkout(str): Specific commit to checkout (optional)
        Returns(Submission): Submission instance
        """
        from .submissions import Submission
        url = f"{self.url}/{entity_id}/submissions"
        self.log.info(f"[SUBMIT] {self._instance_klass.__name__} ({url}): {config}")
        response = self.rest.post(url, json=config)
        return self._make_instance(response, instance_klass=Submission)

    def refresh_tests(self, entity_id: str):
        url = f"{self.url}/{entity_id}/test-files-refresh"
        self.log.info(f"[REFRESH] {self._instance_klass.__name__} ({url})")
        response = self.rest.post(url, {})
        return self._make_instance(response, instance_klass=None)


class Project(Default):
    @property
    def course(self):
        return self.parent

    @property
    def submissions(self):
        from kontr_api.resources.submissions import Submissions
        return Submissions(self)

    @property
    def project_config(self) -> ProjectConfigs:
        """Gets project config
        Returns(ProjectConfigs): Projects config client

        """
        return ProjectConfigs(self)

    def submit(self, config: dict):
        return self.client.submit(self.entity_id, config)

    def refresh_files(self):
        return self.client.refresh_files(self.entity_id)

