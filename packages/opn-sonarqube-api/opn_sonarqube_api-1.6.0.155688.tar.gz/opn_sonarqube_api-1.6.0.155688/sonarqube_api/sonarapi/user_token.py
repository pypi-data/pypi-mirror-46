class SonarAPIUserToken(object):
    #Endpoint for permission templates
    USER_TOKEN_GENERATE_ENDPOINT = '/api/user_tokens/generate'
    USER_TOKEN_SEARCH_ENDPOINT = '/api/user_tokens/search'

    def __init__(self, api=None):
        self._api = api

    def generate_token(self, token_name, user_login):
        """
        Create user token.

        :param token_name: name of the token to generate
        :param user_login: user to generate token for
        :return: request response
        """
        # Build main data to post
        data = {
            'name': token_name,
            'login': user_login
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.USER_TOKEN_GENERATE_ENDPOINT, **data)
        return res

    def search_token(self, user_login):
        """
        List existing token for user.
        """
        data = {
            'login': user_login
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.USER_TOKEN_SEARCH_ENDPOINT, **data)
        return res
