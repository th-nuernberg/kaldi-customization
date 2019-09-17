# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.test import BaseTestCase


class TestResourceController(BaseTestCase):
    """ResourceController integration test stubs"""

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


if __name__ == '__main__':
    unittest.main()
