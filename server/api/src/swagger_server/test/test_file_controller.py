# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

java.io.File  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    def test_create_file(self):
        """Test case for create_file

        Create/Upload a new file
        """
        body = (BytesIO(b'some file data'), 'file.txt')
        response = self.client.open(
            '/api/v1/file',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_file_by_uuid(self):
        """Test case for get_file_by_uuid

        Find file by UUID
        """
        response = self.client.open(
            '/api/v1/file/{fileUuid}'.format(fileUuid='fileUuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
