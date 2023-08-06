from pathlib import Path

import appdirs

AUTHOR = 'muni'
APP_NAME = 'kontrctl'


class ConfigStore(object):
    def __init__(self):
        app_config = dict(appauthor=AUTHOR, appname=APP_NAME)
        self._user_data = Path(appdirs.user_data_dir(**app_config))
        self._user_config = Path(appdirs.user_config_dir(**app_config))

    @property
    def user_data(self):
        return self._user_data

    @property
    def user_config(self):
        return self._user_config

