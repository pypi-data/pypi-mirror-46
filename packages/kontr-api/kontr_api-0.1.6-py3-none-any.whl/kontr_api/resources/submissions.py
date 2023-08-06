import logging

from kontr_api.resources.default import Default, Defaults
from kontr_api.resources.submission_files import SubmissionFiles

log = logging.getLogger(__name__)


class Submissions(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Submission)

    @property
    def url(self):
        return f"{self.kontr_client.url}/submissions"

    def create(self, config):
        """Creates new resource
        Args:
            config(dict): Resource parameters
        Returns: Created instance

        """
        url = self.parent.url + '/submissions'
        self.log.info(f"[CREATE] Submission ({url}): {config}")
        response = self.rest.post(url, json=config)
        return self._make_instance(response)

    def resubmit(self, sid: str):
        url = f"{self.url}/{sid}/resubmit"
        return self.rest.post(url)

    def cancel(self, sid: str):
        url = f"{self.url}/{sid}/cancel"
        return self.rest.post(url)

    def stats(self, sid: str):
        url = f"{self.url}/{sid}/stats"
        return self.rest.get(url)


class Submission(Default):
    @property
    def sources(self) -> SubmissionFiles:
        return SubmissionFiles(self, 'sources')

    @property
    def test_files(self) -> SubmissionFiles:
        return SubmissionFiles(self, 'test_files')

    @property
    def results(self) -> SubmissionFiles:
        return SubmissionFiles(self, 'results')

    def resubmit(self):
        return self.client.resubmit(self.entity_id)

    def cancel(self):
        return self.client.cancel(self.entity_id)

    def stats(self):
        return self.client.stats(self.entity_id)
