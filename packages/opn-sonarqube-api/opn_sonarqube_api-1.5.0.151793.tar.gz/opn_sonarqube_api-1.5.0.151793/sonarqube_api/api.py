"""
This module contains the SonarAPIHandler, used for communicating with the
SonarQube server web service API.
"""

import requests

from .exceptions import ClientError, AuthError, ValidationError, ServerError

from sonarapi.groups import SonarAPIGroup
from sonarapi.permissions import SonarAPIPermissionTemplates
from sonarapi.user_token import SonarAPIUserToken
from sonarapi.users import SonarAPIUser
from sonarapi.metrics import SonarAPIMetrics
from sonarapi.qualityprofiles import SonarAPIQualityProfile
from sonarapi.resources import SonarAPIResources
from sonarapi.rules import SonarAPIRules
from sonarapi.settings import SonarAPISettings

class SonarAPIHandler(object):
    """
    Adapter for SonarQube's web service API.
    """
    # Default host is local
    DEFAULT_HOST = 'http://localhost'
    DEFAULT_PORT = 9000
    DEFAULT_BASE_PATH = ''

    # Endpoint for resources and rules
    AUTH_VALIDATION_ENDPOINT = '/api/authentication/validate'


    def __init__(self, host=None, port=None, user=None, password=None,
                 base_path=None, token=None):
        """
        Set connection info and session, including auth (if user+password
        and/or auth token were provided).
        """
        self._host = host or self.DEFAULT_HOST
        self._port = port or self.DEFAULT_PORT
        self._base_path = base_path or self.DEFAULT_BASE_PATH
        self._session = requests.Session()

        # Prefer revocable authentication token over username/password if
        # both are provided
        if token:
            self._session.auth = token, ''
        elif user and password:
            self._session.auth = user, password

        self._group = SonarAPIGroup(api=self)
        self._permissions = SonarAPIPermissionTemplates(api=self)
        self._user_token = SonarAPIUserToken(api=self)
        self._user = SonarAPIUser(api=self)
        self._metrics = SonarAPIMetrics(api=self)
        self._qualityprofile = SonarAPIQualityProfile(api=self)
        self._resources = SonarAPIResources(api=self)
        self._rules = SonarAPIRules(api=self)
        self._settings = SonarAPISettings(api=self)

    def _get_url(self, endpoint):
        """
        Return the complete url including host and port for a given endpoint.

        :param endpoint: service endpoint as str
        :return: complete url (including host and port) as str
        """
        return '{}:{}{}{}'.format(self._host, self._port, self._base_path, endpoint)

    def _make_call(self, method, endpoint, **data):
        """
        Make the call to the service with the given method, queryset and data,
        using the initial session.

        Note: data is not passed as a single dictionary for better testability
        (see https://github.com/kako-nawao/python-sonarqube-api/issues/15).

        :param method: http method (get, post, put, patch)
        :param endpoint: relative url to make the call
        :param data: queryset or body
        :return: response
        """
        # Get method and make the call
        call = getattr(self._session, method.lower())
        url = self._get_url(endpoint)
        res = call(url, data=data or {})

        # Analyse response status and return or raise exception
        # Note: redirects are followed automatically by requests
        if res.status_code < 300:
            # OK, return http response
            return res

        elif res.status_code == 400:
            # Validation error
            msg = ', '.join(e['msg'] for e in res.json()['errors'])
            raise ValidationError(msg)

        elif res.status_code in (401, 403):
            # Auth error
            raise AuthError(res.reason)

        elif res.status_code < 500:
            # Other 4xx, generic client error
            raise ClientError(res.reason)

        else:
            # 5xx is server error
            raise ServerError(res.reason)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #
    # #  API
    # #

    def validate_authentication(self):
        """
        Validate the authentication credentials passed on client initialization.
        This can be used to test the connection, since API always returns 200.

        :return: True if valid
        """
        res = self._make_call('get', self.AUTH_VALIDATION_ENDPOINT).json()
        return res.get('valid', False)

    ## user group API
    def create_group(self, group_name, group_description):
        return self._group.create_group(group_name, group_description)

    def search_group(self, group_name):
        return self._group.search_group(group_name)

    def update_group(self, group_id, group_name, group_description):
        return self._group.update_group(group_id, group_name, group_description)

    def delete_group(self, group_id):
        return self._group.delete_group(group_id)
    
    ## permissions API
    def create_permission_template(self, template_name, template_description, projectKeyPattern):
        return self._permissions.create_template(template_name, template_description, projectKeyPattern)

    def update_permission_template(self, template_id, template_name, template_description, projectKeyPattern):
        return self._permissions.update_template(template_id, template_name, template_description, projectKeyPattern)

    def search_permission_template(self, template_name):
        return self._permissions.search_template(template_name)

    def delete_permission_template(self, template_id):
        return self._permissions.delete_template(template_id)

    def add_group_to_template(self, template_id, group_name, permission):
        return self._permissions.add_group_to_template(template_id, group_name, permission)

    def list_groups_of_template(self, template_id):
        return self._permissions.list_groups_of_template(template_id)

    def remove_group_from_template(self, template_id, group_name, permission):
        return self._permissions.remove_group_from_template(template_id, group_name, permission)

    ## user token
    def generate_token(self, token_name, user_login):
        """
        Create user token.

        :param token_name: name of the token to generate
        :param user_login: user to generate token for
        :return: request response
        """
        return self._user_token.generate_token(token_name, user_login)

    def user_tokens(self, user_login):
        """
        List existing token for user.
        :param user_login: user to generate token for
        """
        return self._user_token.search(user_login)

    # user
    def user_current(self):
        return self._user.current()

     # metrics
    def get_metrics(self, fields=None):
        """
        Yield defined metrics.

        :param fields: iterable or comma-separated string of field names
        :return: generator that yields metric data dicts
        """
        return self._metrics.get_metrics(fields)

    # quality profile
    def activate_rule(self, key, profile_key, reset=False, severity=None,
                      **params):
        """
        Activate a rule for a given quality profile.

        :param key: key of the rule
        :param profile_key: key of the profile
        :param reset: reset severity and params to default
        :param severity: severity of rule for given profile
        :param params: customized parameters for the rule
        :return: request response
        """
        return self._qualityprofile.activate_rule(key, profile_key, reset, severity, **params)

     # resources
    def get_resources_debt(self, resource=None, categories=None,
                           include_trends=False, include_modules=False):
        """
        Yield first-level resources with debt by category (aka. characteristic).

        :param resource: key of the resource to select
        :param categories: iterable of debt characteristics by name
        :param include_trends: include differential values for leak periods
        :param include_modules: include modules data
        :return: generator that yields resource debt data dicts
        """
        return self._resources.get_resources_debt(resource, categories,
                           include_trends, include_modules)

    def get_resources_metrics(self, resource=None, metrics=None,
                              include_trends=False, include_modules=False):
        """
        Yield first-level resources with generic metrics.

        :param resource: key of the resource to select
        :param metrics: iterable of metrics to return by name
        :param include_trends: include differential values for leak periods
        :param include_modules: include modules data
        :return: generator that yields resource metrics data dicts
        """
        return self._resources.get_resources_metrics(resource, metrics,
                              include_trends, include_modules)

    # rules
    def create_rule(self, key, name, description, message, xpath, severity,
                    status, template_key):
        """
        Create a a custom rule.

        :param key: key of the rule to create
        :param name: name of the rule
        :param description: markdown description of the rule
        :param message: issue message (title) for the rule
        :param xpath: xpath query to select the violation code
        :param severity: default severity for the rule
        :param status: status of the rule
        :param template_key: key of the template from which rule is created
        :return: request response
        """
        return self._rules.create_rule(key, name, description, message, xpath, severity,
                    status, template_key)

    def get_rules(self, active_only=False, profile=None, languages=None,
                  custom_only=False):
        """
        Yield rules in status ready, that are not template rules.

        :param active_only: filter only active rules
        :param profile: key of profile to filter rules
        :param languages: key of languages to filter rules
        :param custom_only: filter only custom rules
        :return: generator that yields rule data dicts
        """
        return self._rules.get_rules(active_only, profile, languages,
                  custom_only)

    def get_resources_full_data(self, resource=None, metrics=None,
                                categories=None, include_trends=False,
                                include_modules=False):
        """
        Yield first-level resources with merged generic and debt metrics.

        :param resource: key of the resource to select
        :param metrics: iterable of metrics to return by name
        :param categories: iterable of debt characteristics by name
        :param include_trends: include differential values for leak periods
        :param include_modules: include modules data
        :return: generator that yields resource metrics and debt data dicts
        """
        return self._resources.get_resources_full_data(resource, metrics,
                                categories, include_trends,
                                include_modules)

    def setting(self, key, value):
        """
        Create/update setting.

        :param key: name of the setting to update
        :param value: value to set
        :return: request response
        """
        return self._settings.set(key, value)

    def getting(self, key):
        """
        Create/update setting.

        :param key: name of the setting to get
        :return: request response
        """
        return self._settings.get(key)
