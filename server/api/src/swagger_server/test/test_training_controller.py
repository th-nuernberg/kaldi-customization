# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.binary import Binary  # noqa: E501
from swagger_server.models.training_status import TrainingStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTrainingController(BaseTestCase):
    """TrainingController integration test stubs"""

    def test_download_training_result(self):
        """Test case for download_training_result

        Find project training results by UUID
        """
        response = self.client.open(
            '/api/v1/project/{projectUuid}/training'.format(projectUuid='projectUuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_train_project(self):
        """Test case for train_project

        Train current project
        """
        response = self.client.open(
            '/api/v1/project/{projectUuid}/training'.format(projectUuid='projectUuid_example'),
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
