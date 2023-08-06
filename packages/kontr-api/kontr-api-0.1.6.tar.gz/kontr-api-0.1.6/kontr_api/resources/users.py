import logging

from kontr_api.resources.default import Default, Defaults

log = logging.getLogger(__name__)


class Users(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=User)

    def set_password(self, new: str, current: str = None, eid=None):
        """Updates instance
        Args:
            current(str): Current password
            new(str): New password
            eid(str): Entity id
        """
        url = self._get_resource_url(eid) + '/password'
        self.log.info(f"[UPDATE] User's Password ({url})")
        data = {'new_password': new}
        if current:
            data['old_password'] = current
        self.rest.put(url, json=data)


class User(Default):
    @property
    def submissions(self):
        from kontr_api.resources.submissions import Submissions
        return Submissions(self)

    @property
    def courses(self):
        from kontr_api.resources.courses import Courses
        return Courses(self)

    @property
    def secrets(self):
        from kontr_api.resources.secrets import Secrets
        return Secrets(self)

    def set_password(self, new: str, current: str = None):
        config = {'new': new, 'current': current}
        self.client.set_password(**config, eid=self.entity_id)
