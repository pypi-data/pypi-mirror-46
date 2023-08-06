from base import devops_client_exception
from base import devops_base

# _attribute_map = {
#        'abbreviation': {'key': 'abbreviation', 'type': 'str'},
#        'default_team_image_url': {'key': 'defaultTeamImageUrl', 'type': 'str'},
#        'description': {'key': 'description', 'type': 'str'},
#        'id': {'key': 'id', 'type': 'str'},
#        'name': {'key': 'name', 'type': 'str'},
#        'revision': {'key': 'revision', 'type': 'long'},
#        'state': {'key': 'state', 'type': 'object'},
#        'url': {'key': 'url', 'type': 'str'},
#        'visibility': {'key': 'visibility', 'type': 'object'}
# }


class devops_projects(devops_base):
    """ spin up connection from base and create client, and get list of projects"""
    def __init__(self):
        # init base class (brings up connections etc)
        super().__init__()
        try:
            self._core_client = self._connection.clients.get_core_client()
        except Exception as could_not_get_client:
            print(f"Could Not Get Devops Client {str(could_not_get_client)}")

        try:
            self._projects = self._core_client.get_projects()
        except Exception as could_not_get_project_list:
            print(f"Could Not Get Project List {str(could_not_get_project_list)}")

    def get_project_from_id(self, project_id):
        """return project object from id"""
        for proj in self._projects:
            if proj.__dict__['id'] == project_id:
                return devops_project(proj.__dict__)
        raise devops_client_exception(f"Couldn't find project {project_id}")

    def get_project_from_name(self, project_name):
        """ return project object from name"""
        for proj in self._projects:
            if proj.__dict__['name'] == project_name:
                return devops_project(proj.__dict__)
        raise devops_client_exception(f"Couldn't find project {project_name}")


class devops_project():
    """ holder object for project information """
    def __init__(self, project_object):
        self._project = project_object
        self.id = self._project['id']
        self.name = self._project['name']

    def __str__(self):
        return f"Devops Project: {self._project['name']}"

    __repr__ = __str__
