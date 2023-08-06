from .policy_types import policy_types
from .base import devops_client_exception
from .projects import devops_project


class policy(policy_types):
    def __init__(self, project):
        """ basic policy interaction """
        if not isinstance(project, devops_project):
            raise devops_client_exception("Project Parameter should be an instance of devops_project")
        super().__init__()
        self._projectid = project.id

    def get_policies(self, project, scope=None, policy_type=None):
        """ return a full list of policy_configuration objects for every policy in the project """
        out_arr = []
        try:
            pol_configs = self._policy_client.get_policy_configurations(self._projectid, scope, policy_type)
            for pol_config in pol_configs:
                out_arr.append(policy_configuration(pol_config.__dict__))
        except Exception as could_not_get_policies:
            raise devops_client_exception(f"Could get policy list - {str(could_not_get_policies)}")
        return out_arr

    def create_or_update_policy_configuration(self, policy_builder):
        """create or update policy based on the policy builder object. will update multiple policies that apply if they apply exactly
        and are the correct policytype
        """
        try:
            existing_policies = self.__is_there_an_existing_policy_for_that(policy_builder)
            if not existing_policies:
                return self._policy_client.create_policy_configuration(policy_builder._pyobject, self._projectid)
            out_arr = []
            for pol in existing_policies:
                out_arr.append(self._policy_client.update_policy_configuration(policy_builder._pyobject, self._projectid, pol.id))
            return out_arr
        except Exception as could_not_create_policy:
            raise devops_client_exception(f"Could not apply policy - {str(could_not_create_policy)}")

    def match_scope(self, policy_builder, scope_list):
        """ does the scope object supplied have an exact match for the repo and ref and have scope 'Exact' i.e not partial, return true/false"""
        ref = policy_builder.ref.name
        for scope in scope_list:
            if scope['refName'] == ref and scope['matchKind'] == 'Exact' and scope['repositoryId'] == policy_builder.ref.repo_id:
                return True
        return False

    def is_there_an_existing_policy_for_that(self, policy_builder):
        """ if there is an existing policy for that exactly that ref, find it and return them else return False

        This can return MULTIPLE policies because for some reason even though you can't set that in the gui
        for some reason you can with the API, how this displays I don't know but to be safe we assume that if you
        want to set an 'EXACT' scope for a policy we will set it on all policies that match that.
        in short don't be too clever with the policies api or things will end up stupid."""
        matched_policies = []
        pol_type_id = policy_builder.policy_type.id
        pol_list = self.__get_policies(policy_builder.project.id)
        for pol in pol_list:
            if pol.get_type_id() == pol_type_id:
                if self.__match_scope(policy_builder, pol.get_scope()):
                    matched_policies.append(pol)
        if not matched_policies:
            return False
        return matched_policies

    __get_policies = get_policies
    __create_or_update_policy_configuration = create_or_update_policy_configuration
    __is_there_an_existing_policy_for_that = is_there_an_existing_policy_for_that
    __match_scope = match_scope


class policy_configuration():
    """ object to represent a policy configuration returned from devops"""
    def __init__(self, pol_config_data):
        self._data = pol_config_data
        self._settings = pol_config_data['settings']
        self.id = pol_config_data['id']
        self._type = pol_config_data['type']

    def get_scope(self):
        return self._settings['scope']

    def get_type_id(self):
        return self._type.id

    def __str__(self):
        return f"Policy: {self._settings}\n"

    __get_scope = get_scope
    __repr__ = __str__
