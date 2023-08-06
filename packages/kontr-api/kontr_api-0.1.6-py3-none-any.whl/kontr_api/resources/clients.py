from kontr_api.resources.default import Defaults, Default


class Clients(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Client)

    def me(self):
        url = self.kontr_client.url + '/client'
        self.log.debug(f"[READ] Client ({url})")
        response = self.rest.get(url)
        return self._make_instance(response)


class Client(Default):
    @property
    def secrets(self):
        from kontr_api.resources.secrets import Secrets
        return Secrets(self)
