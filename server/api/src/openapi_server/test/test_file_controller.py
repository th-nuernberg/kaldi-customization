# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

java.io.File  # noqa: E501
from openapi_server.test import BaseTestCase


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    @unittest.skip("*/* not supported by Connexion. Use application/json instead. See https://github.com/zalando/connexion/pull/760")
    def test_create_file(self):
        """Test case for create_file

        Create/Upload a new file
        """
        body = (BytesIO(b'some file data'), 'file.txt')
        headers = { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/file',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_file_by_uuid(self):
        """Test case for get_file_by_uuid

        Find file by UUID
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/file/{file_uuid}'.format(file_uuid='file_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
