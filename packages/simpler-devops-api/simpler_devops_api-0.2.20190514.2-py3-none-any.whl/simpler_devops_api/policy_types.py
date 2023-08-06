from fuzzywuzzy import fuzz
from .base import devops_client_exception
from .base import devops_base
from .projects import devops_project


class policy_type:
    """PolicyType.
    :param display_name: Display name of the policy type.

    :type display_name: str

    :param id: The policy type ID.

    :type id: str

    :param url: The URL where the policy type can be retrieved.

    :type url: str

    :param _links: The links to other objects related to this object.

    :type _links: :class:`ReferenceLinks <azure.devops.v5_1.policy.models.ReferenceLinks>`

    :param description: Detailed description of the policy type.

    :type description: str
    """
    def __init__(self, pol_type_data):
        self._data = pol_type_data
        self.display_name = pol_type_data['display_name']
        self.id = pol_type_data['id']
        self.description = pol_type_data['description']

    def __str__(self):
        return f"Policy: {self.display_name} - ID: {self.id} || {self.description}\n"

    __repr__ = __str__


class policy_types(devops_base):
    """ spin up connection from base and create client, and get list of projects"""
    def __init__(self):
        # init base class (brings up connections etc)
        super().__init__()
        try:
            self._policy_client = self._connection.get_client("azure.devops.v5_1.policy.policy_client.PolicyClient")
        except Exception as could_not_get_client:
            print(f"Could Not Get Devops Client {str(could_not_get_client)}")

    def get_policy_types(self, project):
        """ return a list of policy type objects """
        if not isinstance(project, devops_project):
            raise devops_client_exception("Project Parameter should be an instance of devops_project")
        out_arr = []
        pols = []
        try:
            pols = self._policy_client.get_policy_types(project.id)
        except Exception as could_not_get_policy_types:
            print(f"Could Not Get Policy Types {str(could_not_get_policy_types)}")
        for pol in pols:
            out_arr.append(policy_type(pol.__dict__))
        return out_arr

    def get_policy_type_by_name(self, policy_name, project):
        """ use fuzzywuzzy to match policy type against name for legibility """
        if not isinstance(project, devops_project):
            raise devops_client_exception("Project Parameter should be an instance of devops_project")
        pols = []

        try:
            pols = self._policy_client.get_policy_types(project.id)
        except Exception as could_not_get_policy_types:
            print(f"Could Not Get Policy Types {str(could_not_get_policy_types)}")

        for pol in pols:
            ratio = fuzz.partial_ratio(pol.__dict__['display_name'], policy_name)
            if ratio > 90:
                return policy_type(pol.__dict__)
        raise devops_client_exception(f"Could Not Find Policy Type for Name {policy_name} using fuzzy matching")
