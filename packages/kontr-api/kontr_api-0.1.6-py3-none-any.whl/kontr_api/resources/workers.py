from kontr_api.resources.default import Default, Defaults
from kontr_api.resources.secrets import Secrets


class Workers(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Worker)

    def status(self, wid):
        url = self._get_resource_url(wid) + "/status"
        self.log.debug(f"[READ] Worker status ({url})")
        response = self.rest.get(url)
        return self._make_json(response)


class Worker(Default):
    @property
    def status(self):
        return self.client.status(self.entity_id)

    @property
    def secrets(self) -> Secrets:
        return Secrets(self)
