import logging
from typing import Optional

from requests import Response

from kontr_api.auth import AuthBase
from kontr_api.rest_client import KontrRestClient


class Defaults(object):
    def __init__(self, parent, instance_klass=None):
        self._parent = parent
        self._instance_klass = instance_klass
        self.log = logging.getLogger(self.__module__)
        self._url = None

    @property
    def url(self) -> str:
        """Gets url for the resource collection
        Returns(str): Url for the resource collection
        """
        if self._url is None:
            self._url = self.parent.url + f"/{str(self.__class__.__name__.lower())}"
        return self._url

    @property
    def kontr_client(self):
        """Gets instance of the Kontr Client
        Returns(KontrClient): Kontr client instance
        """
        return self.parent.kontr_client

    @property
    def parent(self):
        """Gets parent resource
        Returns: Parent resource

        """
        return self._parent

    @property
    def auth(self) -> AuthBase:
        """Gets auth base
        Returns(AuthBase): AuthBase instance

        """
        return self.parent.auth

    @property
    def rest(self) -> KontrRestClient:
        """Gets rest client instance
        Returns(KontrRestClient): Kontr rest client instance
        """
        return self.kontr_client.rest

    def create(self, config, **kwargs):
        """Creates new resource
        Args:
            config(dict): Resource parameters
        Returns: Created instance

        """
        url = self.url
        self.log.info(f"[CREATE] {self._instance_class_name} ({url}): {config}")
        response = self.rest.post(url, json=config, **kwargs)
        return self._make_instance(response)

    def list(self, *args, **kwargs):
        """Lists all the instances in kontr
        Returns(List): List of all instances
        """
        entities = self._list(*args, **kwargs)
        self.log.debug(f"[RES] List: {entities}")
        return entities

    def update(self, config, eid: str = None, **kwargs):
        """Updates instance
        Args:
            config(dict): Entity configuration
            eid(str): Entity id
        """
        url = self._get_resource_url(eid)
        self.log.info(f"[UPDATE] {self._instance_class_name}({url}): {config}")
        response = self.rest.put(url, json=config, **kwargs)
        return self._make_instance(response)

    def read(self, eid: str = None, **kwargs):
        """Gets an instance
        Args:
            eid(str): Entity id

        Returns: Entity instance
        """
        url = self._get_resource_url(eid)
        self.log.debug(f"[READ] {self._instance_class_name}({url})")
        response = self.rest.get(url, **kwargs)
        return self._make_instance(response)

    def delete(self, eid: str = None, **kwargs):
        """Deletes entity
        Args:
            eid(str): Entity id
        Returns:

        """
        url = self._get_resource_url(eid)
        self.log.info(f"[DELETE] {self._instance_class_name}({url})")
        response = self.rest.delete(url, **kwargs)
        return self._make_instance(response)

    def _list(self, *args, **kwargs):
        url = self.url
        self.log.info(f"[LIST] {self._instance_class_name} ({url})")
        response = self.rest.get(url, *args, **kwargs)
        return self._make_instance(response, is_list=True, should_log=False)

    def _get_resource_url(self, eid: str) -> str:
        """Gets resource with `eid`
        Args:
            eid(str): Entity id
        Returns(str): Full url
        """
        return f'{self.url}/{eid}' if eid else f'{self.url}'

    @property
    def _instance_class_name(self):
        if self._instance_klass is None:
            return 'Object'
        return self._instance_klass.__name__

    def _make_json(self, response: Response) -> Optional[dict]:
        if response is None:
            return None
        return response.json() if len(response.content) > 0 else None

    def _make_instance(self, response: Response, should_log=True, is_list=False,
                       instance_klass=None, raw=False):
        """Creates instance
        Args:
            response(Response): Response
            should_log(bool): Whether to log the result
            is_list(bool): Whether response is a list
            instance_klass: Instance class
        Returns: New instance wrapper

        """
        data = self._make_json(response) if not raw else response.content
        if data is None:
            return None
        instance_klass = instance_klass or self._instance_klass
        if instance_klass is None or issubclass(instance_klass, dict):
            if should_log:
                self.log.debug(f"[INST] Instance: {data}")
            return data
        instance = instance_klass(self, data) if not is_list \
            else [instance_klass(self, item) for item in data]
        if should_log:
            self.log.debug(f"[INST] Instance: {instance}")
        return instance

    def __getitem__(self, item):
        return self.read(item)


class Default(object):
    def __init__(self, client: Defaults, config: dict = None, eid: str = None):
        """Creates default response
        Args:
            client: Collection instance
            config(dict): Configuration
            eid(str): Entity id
        """
        self._id = eid
        self._config = config
        self._client = client

    @property
    def id(self):
        return self.config['id']

    @property
    def kontr_client(self):
        """Gets kontr client instance
        Returns(KontrClient): Kontr client instance
        """
        return self.client.kontr_client

    @property
    def config(self) -> dict:
        """Gets config instance for the entity
        Returns(dict): Dict representation of the entity
        """
        return self._config

    @config.setter
    def config(self, value: dict):
        """Sets config
        Args:
            value(dict): New configuration
        """
        self._config = value

    @property
    def entity_id(self) -> str:
        """Gets entity id
        Returns(str): Entity id
        """
        return self.config.get('id') or self._id

    @property
    def entity_selector(self) -> str:
        """Entity selector
        Returns(str): Entity selector
        """
        return 'code_name'

    @property
    def rest(self) -> KontrRestClient:
        """Gets rest client instance
        Returns(KontrRestClient): Kontr rest client instance
        """
        return self.client.rest

    @property
    def client(self):
        """Gets collection instance
        Returns:

        """
        return self._client

    @property
    def url(self) -> str:
        """Gets url instance
        Returns(str): Url
        """
        return self.client.url + f"/{self.entity_id}"

    @property
    def parent(self):
        """Gets parent resource
        Returns: Parent resource
        """
        return self.client.parent

    def read(self, **kwargs):
        """Reads configuration
        Returns: Entity instance
        """
        read_entity = self.client.read(self.entity_id, **kwargs)
        self.config = read_entity.config
        return self

    def delete(self, **kwargs):
        """Deletes resource
        """
        self.client.delete(eid=self.entity_id, **kwargs)

    def update(self, config: dict = None, **kwargs):
        """Updates resource
        Args:
            config(dict): Changes in the configuration
        """
        if config is not None:
            self.config.update(config)
        self.client.update(eid=self.entity_id, config=self.config, **kwargs)
        self.read()
        return self

    def __getitem__(self, item: str):
        return self.config.get(item)

    def __setitem__(self, key: str, value):
        self.config[key] = value

    def __str__(self):
        return f'{self.__class__.__name__} ({self.config})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.entity_id == other.entity_id
