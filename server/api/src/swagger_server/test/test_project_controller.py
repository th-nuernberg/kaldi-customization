# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.binary import Binary  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server.models.training_status import TrainingStatus  # noqa: E501
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

    def test_download_training_result(self):
        """Test case for download_training_result

        Find project training results by UUID
        """
        response = self.client.open(
            '/api/v1/project/{projectUuid}/training'.format(projectUuid='projectUuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project_by_uuid(self):
        """Test case for get_project_by_uuid

        Find project by UUID
        """
        response = self.client.open(
            '/api/v1/project/{projectUuid}'.format(projectUuid='projectUuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_train_project(self):
        """Test case for train_project

        Train current project
        """
        response = self.client.open(
            '/api/v1/project/{projectUuid}/training'.format(projectUuid='projectUuid_example'),
            method='POST',
            content_type='application/json')
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
