from kontr_api.resources.default import Defaults


class SubmissionFiles(Defaults):
    def __init__(self, parent, subpath=None):
        super().__init__(parent)
        self._subpath = subpath

    @property
    def url(self):
        return f"{self.parent.url}/files/{self._subpath}"

    def upload(self, path=None):
        url = self.url
        self.log.debug(f'[FILES] Upload files ({url}) <- {path}')
        return self.rest.upload_file(url, path)

    def download(self, path=None):
        url = self.url
        self.log.debug(f'[FILES] Download files ({url}) -> {path}')
        return self.rest.download_file(url, path)

    def get(self, path=None):
        url = self.url
        self.log.debug(f'[FILES] Get sources ({url}) {path}')
        params = dict(path=path)
        return self.rest.get(url, params=params)

    def content(self, path):
        return self.get(path).content.decode('utf-8')

    def tree(self):
        url = self.url + '/tree'
        self.log.debug(f'[FILES] Get tree ({url})')
        response = self.rest.get(url)
        return response.json()
