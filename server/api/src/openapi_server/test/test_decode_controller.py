# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.audio import Audio  # noqa: E501
from openapi_server.models.callback_object import CallbackObject  # noqa: E501
from openapi_server.models.decode_audio import DecodeAudio  # noqa: E501
from openapi_server.models.decode_session import DecodeSession  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDecodeController(BaseTestCase):
    """DecodeController integration test stubs"""

    def test_assign_audio_to_current_session(self):
        """Test case for assign_audio_to_current_session

        Assign Audio to decoding session
        """
        decode_audio = {
  "transcripts" : [ "{}", "{}" ],
  "session_uuid" : "550e8400-e29b-11d4-a716-446655440000"
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
            data=json.dumps(decode_audio),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_decode_session(self):
        """Test case for create_decode_session

        Create a new decoding session
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/session'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

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

    def test_delete_decode_session(self):
        """Test case for delete_decode_session

        Delete the decoding session
        """
        headers = { 
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/session'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
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

    def test_get_all_decode_sessions(self):
        """Test case for get_all_decode_sessions

        Get the all sessions
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/session'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
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

    def test_get_current_decode_session(self):
        """Test case for get_current_decode_session

        Get the current session
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/session/current'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
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
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/{audio_uuid}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, audio_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_decode_session(self):
        """Test case for get_decode_session

        Get a decode session
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/session/{session_uuid}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, session_uuid=550e8400-e29b-11d4-a716-446655440000),
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

        Commits the decode session for decoding
        """
        callback_object = {
  "url" : "url"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/session/{session_uuid}/commit'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, session_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='PUT',
            headers=headers,
            data=json.dumps(callback_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_unassign_audio_to_current_session(self):
        """Test case for unassign_audio_to_current_session

        Unassign Audio to decoding session
        """
        headers = { 
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/decode/{audio_uuid}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56, audio_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_upload_audio(self):
        """Test case for upload_audio

        Uploads audio
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer special-key',
        }
        data = dict(upfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/v1/audio',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
