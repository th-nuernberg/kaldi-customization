# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.create_project_object import CreateProjectObject  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProjectController(BaseTestCase):
    """ProjectController integration test stubs"""

    def test_create_project(self):
        """Test case for create_project

        Create a new project
        """
        create_project_object = {
  "name" : "MyProject",
  "acoustic_model" : "550e8400-e29b-11d4-a716-446655440000"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project',
            method='POST',
            headers=headers,
            data=json.dumps(create_project_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project_by_uuid(self):
        """Test case for get_project_by_uuid

        Find project by UUID
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_projects(self):
        """Test case for get_projects

        Returns a list of available projects
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
