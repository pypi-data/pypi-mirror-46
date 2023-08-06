class SonarAPIPermissionTemplates(object):
    #Endpoint for permission templates
    PERMISSIONS_TEMPLATE_CREATE_ENDPOINT = '/api/permissions/create_template'
    PERMISSIONS_TEMPLATE_LIST_ENDPOINT = '/api/permissions/search_templates'
    PERMISSIONS_TEMPLATE_DELETE_ENDPOINT = '/api/permissions/delete_template'
    PERMISSIONS_TEMPLATE_UPDATE_ENDPOINT = '/api/permissions/update_template'
    PERMISSIONS_TEMPLATE_GROUPS = '/api/permissions/template_groups'
    PERMISSIONS_TEMPLATE_ADD_GROUP = '/api/permissions/add_group_to_template'
    PERMISSIONS_TEMPLATE_REMOVE_GROUP = '/api/permissions/remove_group_from_template'

    permissions = ['user', 'codeviewer', 'issueadmin', 'admin', 'scan']


    def __init__(self, api=None):
        self._api = api

    def create_template(self, template_name, template_description, projectKeyPattern):
        """
        Create template.

        :param template_name: name of the template
        :param template_description: description of the template
        :param projectKeyPattern: Pattern for the template template
        :return: request response
        """
        # Build main data to post
        data = {
            'name': template_name,
            'description': template_description,
            'projectKeyPattern': projectKeyPattern
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_CREATE_ENDPOINT, **data)
        return res

    def search_template(self, template_name):
        """
        Search template with specified name.

        :param template_name: name of the group
        :return: request response
        """
        # Build main data to post
        data = {
            'q': template_name
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_LIST_ENDPOINT, **data)
        return res

    def delete_template(self, template_id):
        """
        Delete template id.

        :param template_id: id of the template to delete
        :return: request response
        """
        # Build main data to post
        data = {
            'templateId': template_id
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_DELETE_ENDPOINT, **data)
        return res

    def update_template(self, template_id, template_name, template_description, projectKeyPattern):
        """
        update permission template.

        :param template_id: id of the template to update
        :param template_name: new name
        :param template_description: new description
        :param template_description: new description
        :return: request response
        """
        # Build main data to post
        data = {
            'id': template_id,
            'name': template_name,
            'description': template_description,
            'projectKeyPattern': projectKeyPattern
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_UPDATE_ENDPOINT, **data)
        return res

    def list_groups_of_template(self, template_id):
        """
        get permission template's groups.

        :param template_id: id of the template to update
        :return: request response
        """
        # Build main data to post
        data = {
            'templateId': template_id,
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_GROUPS, **data)
        return res

    def add_group_to_template(self, template_id, group_name, permission):
        """
        update permission template.

        :param template_id: id of the template to update
        :param group_name: name of the group to associate
        :param permission: permission to set in ['user', 'codeviewer', 'issueadmin', 'admin', 'scan']
        :return: request response
        """
        # Build main data to post
        data = {
            'templateId': template_id,
            'groupName': group_name,
            'permission': permission
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_ADD_GROUP, **data)
        return res

    def remove_group_from_template(self, template_id, group_name, permission):
        """
        update permission template.

        :param template_id: id of the template to update
        :param group_name: name of the group to associate
        :param permission: permission to unset in ['user', 'codeviewer', 'issueadmin', 'admin', 'scan']
        :return: request response
        """
        # Build main data to post
        data = {
            'templateId': template_id,
            'groupName': group_name,
            'permission': permission
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.PERMISSIONS_TEMPLATE_REMOVE_GROUP, **data)
        return res
