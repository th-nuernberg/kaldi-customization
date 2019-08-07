# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.test import BaseTestCase


class TestResourceController(BaseTestCase):
    """ResourceController integration test stubs"""

    def test_assign_resource_to_training(self):
        """Test case for assign_resource_to_training

        Assign a resource to the training
        """
        inline_object = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/resource'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_create_resource(self):
        """Test case for create_resource

        Create/Upload a new resource
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer special-key',
        }
        data = dict(upfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/v1/resource',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_assigned_resource_from_training(self):
        """Test case for delete_assigned_resource_from_training

        Remove a resource from the training
        """
        headers = { 
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/resource/{resource_uuid}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, resource_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_corpus_of_training_resource(self):
        """Test case for get_corpus_of_training_resource

        Get the corpus of the resource
        """
        headers = { 
            'Accept': 'text/plain',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/corpus'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, resource_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_resource(self):
        """Test case for get_resource

        Returns a list of available resources
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/resource',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_resource_by_uuid(self):
        """Test case for get_resource_by_uuid

        Find resource by UUID
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/resource/{resource_uuid}'.format(resource_uuid='resource_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_resource_data(self):
        """Test case for get_resource_data

        Returns the resource content
        """
        headers = { 
            'Accept': 'image/jpeg',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/resource/{resource_uuid}/data'.format(resource_uuid='resource_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("text/plain not supported by Connexion")
    def test_set_corpus_of_training_resource(self):
        """Test case for set_corpus_of_training_resource

        Set the corpus of the resource
        """
        body = 'body_example'
        headers = { 
            'Content-Type': 'text/plain',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/corpus'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, resource_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='PUT',
            headers=headers,
            data=json.dumps(body),
            content_type='text/plain')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
