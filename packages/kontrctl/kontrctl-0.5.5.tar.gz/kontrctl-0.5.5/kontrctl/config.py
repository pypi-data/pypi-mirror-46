import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

import click
from kontr_api import KontrClient

import kontrctl
import kontrctl.errors

log = logging.getLogger(__name__)


class Entity:
    def __init__(self):
        """Creates abstract entity
        """
        self._config = {}

    @property
    def config(self) -> dict:
        """Gets config instance
        Returns(dict): Dict instance
        """
        return self._config

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, item):
        return self.config.get(item)


class Remote(Entity):
    def __init__(self, remotes: 'Remotes', name: str, url: str, **params):
        """Creates instance of the remote
        Args:
            remotes(Remotes): Remotes instance
            name(str): Name of the remote
            url(str): Url
            **params:
        """
        super().__init__()
        self.remotes = remotes
        self._client = None
        self.config['name'] = name
        self.config['url'] = url
        self.config.update(**params)

    def update(self, save: bool = True):
        """Updates remote
        """
        self.remotes[self.name] = self
        if save:
            self.remotes.save()

    @property
    def name(self) -> str:
        """Gets name
        Returns(str): Name
        """
        return self.config['name']

    @property
    def url(self) -> str:
        """Gets url
        Returns(str): Url
        """
        return self.config['url']

    @property
    def selected_course(self) -> str:
        """Gets selected course
        Returns(str): Selected course
        """
        return self.config.get('selected_course')

    @selected_course.setter
    def selected_course(self, value: str):
        """Sets selected course
        Args:
            value(str): Value instance
        Returns:
        """
        self.config['selected_course'] = value

    @property
    def selected_project(self) -> str:
        """Gets selected course
        Returns(str): Selected course
        """
        return self.config.get('selected_course')

    @selected_project.deleter
    def selected_project(self):
        del self.config['selected_project']

    @selected_course.deleter
    def selected_course(self):
        del self.config['selected_course']

    @selected_project.setter
    def selected_project(self, value: str):
        """Sets selected project
        Args:
            value(str): Value instance
        Returns:
        """
        self.config['selected_project'] = value

    @property
    def kontr_client(self) -> KontrClient:
        """Creates instance of the kontr client
        Returns(KontrClient):
        """
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def __build_config(self) -> dict:
        """Builds config
        Returns(dict): configuration dictionary
        """
        cfg = {'url': self.url}
        if 'access_token' in self.config:
            cfg['access_token'] = self.config['access_token']
        for name in ['access_token', 'refresh_token', 'username', 'password', 'secret']:
            cfg = self.__add_if_not_null(cfg, name)
        return cfg

    def __add_if_not_null(self, cfg: dict, name: str) -> dict:
        """Adds if not null
        Args:
            cfg(dict): Dict instance
            name(str): Name of the entity
        Returns(dict): Updated dict
        """
        if name in self.config:
            cfg[name] = self.config[name]
        return cfg

    def _create_client(self) -> KontrClient:
        """Creates new client instance
        Returns(KontrClient): Kontr client instance
        """
        config = self.__build_config()
        log.debug("Config has been built: %s", config)
        return KontrClient(**config)


class AbstractConfig:
    def __init__(self, fspath: Path = None):
        self._config = None
        self._fspath = fspath

    @property
    def config(self):
        if self._config is None:
            self._config = self._load()
        return self._config

    def load(self):
        self._config = self._load()

    def _load(self):
        if not self._fspath.exists():
            return {}
        with self._fspath.open() as config_file:
            loaded = json.load(config_file)
            log.debug('Loading file (%s): %s', self._fspath, loaded)
            return self.serialize(loaded)

    def save(self):
        if self._config is None:
            return
        if not self._fspath.parent.exists():
            self._fspath.parent.mkdir(parents=True)
        with open(str(self._fspath), 'w') as config_file:
            config_to_save = self.to_dict()
            log.debug("Saving file (%s): %s", self._fspath, config_to_save)
            json.dump(config_to_save, config_file, indent=4)

    def to_dict(self):
        return self.config

    def serialize(self, json_dict: dict) -> dict:
        return json_dict

    def __getitem__(self, item):
        return self.config.get(item)

    def __setitem__(self, key, value):
        self.config[key] = value


class UserConfig(AbstractConfig):
    @property
    def default_remote(self):
        return self.config.get('default_remote')

    @default_remote.setter
    def default_remote(self, remote_name):
        self.config['default_remote'] = remote_name


class Remotes(AbstractConfig):
    def add(self, name, url, **params):
        """Adds remote
        Args:
            name(str): Name of the remote
            url(str): Url to remote
            **params: Optional args

        """
        log.debug("[REMOTE] Adding remote: %s (%s): {%s}", name, url, params)
        self.config[name] = Remote(self, name, url, **params)

    def list(self) -> List[Remote]:
        """List of remotes
        Returns(list): List of remotes
        """
        log.debug("[REMOTE] Listing remotes")
        items = self.config.items()
        return [val for (key, val) in items]

    def delete(self, name):
        """Deletes remote
        Args:
            name(str): Name of the remote
        """
        log.debug("[REMOTE] Deleting remote: %s", name)
        del self.config[name]

    def serialize(self, json_dict: dict) -> dict:
        """Serializes json dict to object
        Args:
            json_dict(dict):
        Returns(dict):
        """
        res = {}
        for (key, val) in json_dict.items():
            config = dict(name=key)
            config.update(val)
            res[key] = Remote(self, **val)
        return res

    def to_dict(self) -> dict:
        """Serializes entity to dict
        Returns(dict):

        """
        result = {}
        for (name, remote) in self.config.items():
            result[name] = remote.config
        return result


class AppConfig:
    APP_NAME = 'kontrctl'

    def __init__(self, **kwargs):
        """Creates application config instance
        """
        user_config = Path(click.get_app_dir(AppConfig.APP_NAME))
        self._config = UserConfig(user_config / 'user_config.json')
        self._remotes = Remotes(user_config / 'remotes.json')
        self._params = kwargs

    @property
    def config(self) -> UserConfig:
        """Gets user config instance
        Returns(UserConfig): User config instance
        """
        return self._config

    @property
    def remotes(self) -> Remotes:
        """Gets remote config
        Returns(Remotes): Remotes instance
        """
        return self._remotes

    @property
    def params(self) -> Dict:
        return self._params

    @property
    def version(self) -> str:
        """Gets current version of the Kontrctl
        Returns(str): Version string
        """
        return kontrctl.__version__

    def save(self):
        """Saves all the configs
        """
        self.config.save()
        self.remotes.save()

    @property
    def remote(self) -> Optional[Remote]:
        remote_name = self.params.get('remote')
        remote_name = remote_name or self.config.default_remote
        if remote_name is None:
            return None
        remote_inst = self.remotes[remote_name]
        if remote_inst is None:
            return None
        return remote_inst
            
