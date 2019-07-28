# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.project import Project  # noqa: E501
from openapi_server.models.training_status import TrainingStatus  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProjectController(BaseTestCase):
    """ProjectController integration test stubs"""

    def test_create_project(self):
        """Test case for create_project

        Create a new project
        """
        body = {
  "owner" : {
    "id" : 0,
    "username" : "username"
  },
  "name" : "name",
  "resources" : [ {
    "name" : "myFile.pdf",
    "uuid" : "1234567890"
  }, {
    "name" : "myFile.pdf",
    "uuid" : "1234567890"
  } ],
  "acoustic_model" : {
    "name" : "name",
    "language" : {
      "name" : "name",
      "id" : 1
    },
    "id" : 6
  },
  "uuid" : "uuid"
}
        headers = { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_training_result(self):
        """Test case for download_training_result

        Find project training results by UUID
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training'.format(project_uuid='project_uuid_example'),
            method='GET',
            headers=headers)
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
            '/api/v1/project/{project_uuid}'.format(project_uuid='project_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_train_project(self):
        """Test case for train_project

        Train current project
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training'.format(project_uuid='project_uuid_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_project(self):
        """Test case for update_project

        Update an existing project
        """
        body = {
  "owner" : {
    "id" : 0,
    "username" : "username"
  },
  "name" : "name",
  "resources" : [ {
    "name" : "myFile.pdf",
    "uuid" : "1234567890"
  }, {
    "name" : "myFile.pdf",
    "uuid" : "1234567890"
  } ],
  "acoustic_model" : {
    "name" : "name",
    "language" : {
      "name" : "name",
      "id" : 1
    },
    "id" : 6
  },
  "uuid" : "uuid"
}
        headers = { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project',
            method='PUT',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
