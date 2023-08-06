from kontr_api.resources.default import Defaults


class Analytics(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=dict)

    def submissions(self, **kwargs):
        url = self.url + "/submissions"
        self.log.debug(f"[READ] Analytics ({url}) - {kwargs}")
        response = self.rest.get(url, **kwargs)
        return self._make_json(response)



