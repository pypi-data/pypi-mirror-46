from kontr_api.resources.default import Default, Defaults
from kontr_api.resources.mixins import ClientAddMixin, ClientAddsMixin, ProjectAddsMixin, \
    ProjectAddMixin


class Groups(Defaults, ClientAddsMixin, ProjectAddsMixin):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Group)


class Group(Default, ClientAddMixin, ProjectAddMixin):
    @property
    def course(self):
        return self.parent