from kontr_api.resources.default import Defaults


class Management(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=dict)

    def status(self, **kwargs):
        url = self.url + "/status"
        self.log.debug(f"[READ] System status ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_json(response)

    def logs_tree(self, **kwargs):
        url = self.url + "/logs"
        self.log.debug(f"[READ] System logs tree ({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_json(response)

    def logs_file(self, path: str, **kwargs) -> str:
        url = self.url + f"/logs"
        self.log.debug(f"[READ] System logs file ({url})")
        response = self.rest.get(url, params={'path': path}, **kwargs)
        return response.content.decode('utf-8')


