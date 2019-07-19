# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create user
        """
        body = User()
        response = self.client.open(
            '/api/v1/user',
            method='POST',
            data=json.dumps(body),
            content_type='*/*')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user

        Logs user into the system
        """
        query_string = [('username', 'username_example'),
                        ('password', 'password_example')]
        response = self.client.open(
            '/api/v1/user/login',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_user(self):
        """Test case for logout_user

        Logs out current logged in user session
        """
        response = self.client.open(
            '/api/v1/user/logout',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
