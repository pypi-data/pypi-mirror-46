from kontr_api.resources.default import Default, Defaults


class Secrets(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Secret)

    @property
    def url(self):
        return f"{self.kontr_client.url}/clients/{self.parent['id']}/secrets"


class Secret(Default):
    pass
