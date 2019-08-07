# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.binary_decode_object import BinaryDecodeObject  # noqa: E501
from openapi_server.models.decode_message import DecodeMessage  # noqa: E501
from openapi_server.models.decode_task_reference import DecodeTaskReference  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDecodeController(BaseTestCase):
    """DecodeController integration test stubs"""

    def test_get_decode_result(self):
        """Test case for get_decode_result

        Get the result of a decoding task
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/{decode_uuid}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, decode_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_decodings(self):
        """Test case for get_decodings

        List of all decodings
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_decode(self):
        """Test case for start_decode

        Decode audio to text
        """
        binary_decode_object = {
  "audio_file" : ""
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='POST',
            headers=headers,
            data=json.dumps(binary_decode_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
