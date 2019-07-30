# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class DecodeMessage(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, uuid=None, transcripts=None):  # noqa: E501
        """DecodeMessage - a model defined in OpenAPI

        :param uuid: The uuid of this DecodeMessage.  # noqa: E501
        :type uuid: str
        :param transcripts: The transcripts of this DecodeMessage.  # noqa: E501
        :type transcripts: List[object]
        """
        self.openapi_types = {
            'uuid': str,
            'transcripts': List[object]
        }

        self.attribute_map = {
            'uuid': 'uuid',
            'transcripts': 'transcripts'
        }

        self._uuid = uuid
        self._transcripts = transcripts

    @classmethod
    def from_dict(cls, dikt) -> 'DecodeMessage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DecodeMessage of this DecodeMessage.  # noqa: E501
        :rtype: DecodeMessage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def uuid(self):
        """Gets the uuid of this DecodeMessage.


        :return: The uuid of this DecodeMessage.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this DecodeMessage.


        :param uuid: The uuid of this DecodeMessage.
        :type uuid: str
        """

        self._uuid = uuid

    @property
    def transcripts(self):
        """Gets the transcripts of this DecodeMessage.


        :return: The transcripts of this DecodeMessage.
        :rtype: List[object]
        """
        return self._transcripts

    @transcripts.setter
    def transcripts(self, transcripts):
        """Sets the transcripts of this DecodeMessage.


        :param transcripts: The transcripts of this DecodeMessage.
        :type transcripts: List[object]
        """

        self._transcripts = transcripts
