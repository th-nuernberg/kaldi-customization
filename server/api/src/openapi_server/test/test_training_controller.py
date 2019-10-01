# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.callback_object import CallbackObject  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.resource_reference_object import ResourceReferenceObject  # noqa: E501
from openapi_server.models.training import Training  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTrainingController(BaseTestCase):
    """TrainingController integration test stubs"""

    def test_assign_resource_to_training(self):
        """Test case for assign_resource_to_training

        Assign a resource to the training
        """
        resource_reference_object = {
  "resource_uuid" : "550e8400-e29b-11d4-a716-446655440000"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/resource'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='POST',
            headers=headers,
            data=json.dumps(resource_reference_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_training(self):
        """Test case for create_training

        Create a new training
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='POST',
            headers=headers)
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

    def test_download_model_for_training(self):
        """Test case for download_model_for_training

        Returns the model
        """
        headers = { 
            'Accept': 'application/zip',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/model'.format(project_uuid='project_uuid_example', training_version=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_corpus_of_training(self):
        """Test case for get_corpus_of_training

        Get the entire corpus of the specified training
        """
        headers = { 
            'Accept': 'text/plain',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/corpus'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='GET',
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

    def test_get_current_training_for_project(self):
        """Test case for get_current_training_for_project

        Get current training
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/current'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_training_by_version(self):
        """Test case for get_training_by_version

        Find project training results by UUID
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_trainings_for_project(self):
        """Test case for get_trainings_for_project

        Lists all Trainings of a Project
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_vocabulary_of_training(self):
        """Test case for get_vocabulary_of_training

        Get the entire vocabulary of the specified training
        """
        headers = { 
            'Accept': 'text/plain',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/project/{project_uuid}/training/{training_version}/vocabulary'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_prepare_training_by_version(self):
        """Test case for prepare_training_by_version

        Prepare the specified training
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
            '/api/v1/project/{project_uuid}/training/{training_version}/prepare'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='PUT',
            headers=headers,
            data=json.dumps(callback_object),
            content_type='application/json')
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

    def test_start_training_by_version(self):
        """Test case for start_training_by_version

        Start the specified training
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
            '/api/v1/project/{project_uuid}/training/{training_version}/enqueue'.format(project_uuid=550e8400-e29b-11d4-a716-446655440000, training_version=56),
            method='PUT',
            headers=headers,
            data=json.dumps(callback_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
