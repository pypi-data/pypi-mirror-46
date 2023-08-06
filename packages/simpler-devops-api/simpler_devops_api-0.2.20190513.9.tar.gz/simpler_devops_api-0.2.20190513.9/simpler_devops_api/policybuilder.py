import json
from base import devops_client_exception
from projects import devops_project
from repos import devops_ref
from policy_types import policy_type


class policy_builder():
    def __init__(self, poltype, project, devopsref, policycontent, scope='Exact', isblocking=False):
        """ build policy object json from setting and objects

        expects params:

        poltype - policy_type object, use policy_types.get_policy_type_by_name()
        project - devops project object use devops_projects.get_project_by_name()
        devopsref - ref(branch) object, use devops_repos.get_repo_from_name().get_ref_by_name()
        policycontent - a python object containing the policy settings (and nothing else), refer to the api spec for examples
        optional named params
        scope - always set to 'Exact'
        isblocking - defaults to False, set to "True" if you want to stop merges etc.
        """
        if not isinstance(policycontent, dict):
            raise devops_client_exception(f"policycontent should be a dictionary object")
        if not isinstance(project, devops_project):
            raise devops_client_exception(f"project should be a devops_project object")
        if not isinstance(devopsref, devops_ref):
            raise devops_client_exception(f"devopsref should be a devops_ref object")
        if not isinstance(poltype, policy_type):
            raise devops_client_exception(f"policytype should be a policy_type object")

        self.policy_type = poltype
        self.project = project
        self.ref = devopsref

        scope_application_object = {
            'repositoryId': devopsref.repo_id,
            'refName': devopsref.name,
            'matchKind': scope
        }

        type_object = {
            'id': poltype.id
        }

        # despite being a valid json object this has to be in an array, for reasons that are entirely undocumented! Hurray!
        base_settings_object = {
            "scope": [scope_application_object]
        }

        settings_object = {**base_settings_object, **policycontent}

        policy_object = {
            'isEnabled': True,
            'isBlocking': isblocking,
            'type': type_object,
            'settings': settings_object
        }

        self._json = json.dumps(policy_object)
        self._pyobject = policy_object
