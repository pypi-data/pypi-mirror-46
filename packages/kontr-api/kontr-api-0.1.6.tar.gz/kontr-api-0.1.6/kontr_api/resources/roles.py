from kontr_api.resources.default import Default, Defaults
from kontr_api.resources.mixins import ClientAddMixin, ClientAddsMixin


class Permissions(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=PermissionsObject)


class PermissionsObject(Default):
    @property
    def role(self) -> 'Role':
        return self.parent

    def update(self, config: dict=None):
        return self.client.update(config)

    def read(self):
        return self.client.read()


class Roles(Defaults, ClientAddsMixin):
    @property
    def clients(self):
        return 'clients'

    def __init__(self, parent):
        super().__init__(parent, instance_klass=Role)


class Role(Default, ClientAddMixin):
    @property
    def course(self):
        return self.parent

    @property
    def permissions(self):
        return Permissions(self)
