import os
import configparser
from appdirs import user_data_dir


class devops_config:
    """ load config from default appdir (using appdirs) or environment variables """
    def __init__(self):
        self._pat = os.environ.get('DEVOPS_PAT')
        self._org_url = os.environ.get('DEVOPS_URL')
        self._config_directory = user_data_dir('simpler_devops_api')

    def get_pat(self):
        if not self._pat:
            return self.__get_config_value_from_file('DEVOPS_PAT')
        return self._pat

    def get_org_url(self):
        if not self._org_url:
            return self.__get_config_value_from_file('DEVOPS_URL')
        return self._org_url

    def get_config_value_from_file(self, value):
        config = configparser.ConfigParser()
        try:
            config.read([os.path.join(self._config_directory, 'devops.ini'), os.path.expanduser('~/.devops.ini')])
        except Exception as could_not_read_config:
            print(f"Could not read config file: {str(could_not_read_config)}")
        return config['DEFAULT'][value]

    __get_config_value_from_file = get_config_value_from_file
