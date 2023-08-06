class SonarAPIQualityProfile(object):
    RULES_ACTIVATION_ENDPOINT = '/api/qualityprofiles/activate_rule'

    def __init__(self, api=None):
        self._api = api

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
        # Build main data to post
        data = {
            'rule_key': key,
            'profile_key': profile_key,
            'reset': reset and 'true' or 'false'
        }

        if not reset:
            # No reset, Add severity if given (if not default will be used?)
            if severity:
                data['severity'] = severity.upper()

            # Add params if we have any
            # Note: sort by key to allow checking easily
            params = ';'.join('{}={}'.format(k, v) for k, v in sorted(params.items()) if v)
            if params:
                data['params'] = params

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.RULES_ACTIVATION_ENDPOINT, **data)
        return res
