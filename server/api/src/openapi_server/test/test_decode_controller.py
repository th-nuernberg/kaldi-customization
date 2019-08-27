# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.audio import Audio  # noqa: E501
from openapi_server.models.audio_reference_object import AudioReferenceObject  # noqa: E501
from openapi_server.models.binary_resource_object import BinaryResourceObject  # noqa: E501
from openapi_server.models.decode_message import DecodeMessage  # noqa: E501
from openapi_server.models.decode_task_reference import DecodeTaskReference  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDecodeController(BaseTestCase):
    """DecodeController integration test stubs"""

    def test_delete_audio_by_uuid(self):
        """Test case for delete_audio_by_uuid

        Delete audio by UUID
        """
        headers = { 
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/audio/{audio_uuid}'.format(audio_uuid='audio_uuid_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_audio(self):
        """Test case for get_all_audio

        Returns a list of available audio
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/audio',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_audio_by_uuid(self):
        """Test case for get_audio_by_uuid

        Find audio by UUID
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/audio/{audio_uuid}'.format(audio_uuid='audio_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_audio_data(self):
        """Test case for get_audio_data

        Returns the audio content
        """
        headers = { 
            'Accept': 'audio/wav',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/audio/{audio_uuid}/data'.format(audio_uuid='audio_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

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
        audio_reference_object = {
  "audio_uuid" : "550e8400-e29b-11d4-a716-446655440000"
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
            data=json.dumps(audio_reference_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_audio(self):
        """Test case for upload_audio

        Uploads audio
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/audio',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
