# coding: utf-8

"""
    Kaldi Customization Server

    Kaldi Customization Server.  # noqa: E501

    The version of the OpenAPI document: 1.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import openapi_client
from openapi_client.api.training_api import TrainingApi  # noqa: E501
from openapi_client.rest import ApiException


class TestTrainingApi(unittest.TestCase):
    """TrainingApi unit test stubs"""

    def setUp(self):
        self.api = openapi_client.api.training_api.TrainingApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_assign_resource_to_training(self):
        """Test case for assign_resource_to_training

        Assign a resource to the training  # noqa: E501
        """
        pass

    def test_create_training(self):
        """Test case for create_training

        Create a new training  # noqa: E501
        """
        pass

    def test_delete_assigned_resource_from_training(self):
        """Test case for delete_assigned_resource_from_training

        Remove a resource from the training  # noqa: E501
        """
        pass

    def test_download_model_for_training(self):
        """Test case for download_model_for_training

        Returns the model  # noqa: E501
        """
        pass

    def test_get_corpus_of_training(self):
        """Test case for get_corpus_of_training

        Get the entire corpus of the specified training  # noqa: E501
        """
        pass

    def test_get_corpus_of_training_resource(self):
        """Test case for get_corpus_of_training_resource

        Get the corpus of the resource  # noqa: E501
        """
        pass

    def test_get_current_training_for_project(self):
        """Test case for get_current_training_for_project

        Get current training  # noqa: E501
        """
        pass

    def test_get_training_by_version(self):
        """Test case for get_training_by_version

        Find project training results by UUID  # noqa: E501
        """
        pass

    def test_get_trainings_for_project(self):
        """Test case for get_trainings_for_project

        Lists all Trainings of a Project  # noqa: E501
        """
        pass

    def test_get_vocabulary_of_training(self):
        """Test case for get_vocabulary_of_training

        Get the entire vocabulary of the specified training  # noqa: E501
        """
        pass

    def test_prepare_training_by_version(self):
        """Test case for prepare_training_by_version

        Prepare the specified training  # noqa: E501
        """
        pass

    def test_set_corpus_of_training_resource(self):
        """Test case for set_corpus_of_training_resource

        Set the corpus of the resource  # noqa: E501
        """
        pass

    def test_start_training_by_version(self):
        """Test case for start_training_by_version

        Start the specified training  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
