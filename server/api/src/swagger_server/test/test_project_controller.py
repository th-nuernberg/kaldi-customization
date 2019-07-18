# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProjectController(BaseTestCase):
    """ProjectController integration test stubs"""

    def test_create_project(self):
        """Test case for create_project

        Create a new project
        """
        body = Project()
        response = self.client.open(
            '/api/v1/project',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_project(self):
        """Test case for delete_project

        Deletes a project
        """
        headers = [('api_key', 'api_key_example')]
        response = self.client.open(
            '/api/v1/project/{projectUuid}'.format(project_uuid='project_uuid_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project_by_uuid(self):
        """Test case for get_project_by_uuid

        Find project by UUID
        """
        response = self.client.open(
            '/api/v1/project/{projectUuid}'.format(project_uuid='project_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_project(self):
        """Test case for update_project

        Update an existing project
        """
        body = Project()
        response = self.client.open(
            '/api/v1/project',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
