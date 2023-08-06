from devops_config import devops_config
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication


class devops_client_exception(Exception):
    """ custom exception to allow sensible handling """
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class devops_base:
    """ base object for interacting with devops """
    def __init__(self):
        self._config_object = devops_config()
        try:
            self._credentials = BasicAuthentication('', self._config_object.get_pat())
            self._connection = Connection(base_url=self._config_object.get_org_url(), creds=self._credentials)
        except Exception as could_not_connect:
            print(f"Could Not Connect to Devops {str(could_not_connect)}")
