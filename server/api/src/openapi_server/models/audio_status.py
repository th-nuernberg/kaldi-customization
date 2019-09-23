# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class AudioStatus(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    Upload_InProgress = "100"
    Upload_Failure = "190"
    Preparable = "200"
    AudioPrep_Enqueued = "210"
    AudioPrep_InProgress = "220"
    AudioPrep_Failure = "290"
    Decodable = "300"

    def __init__(self):  # noqa: E501
        """AudioStatus - a model defined in OpenAPI

        """
        self.openapi_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'AudioStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AudioStatus of this AudioStatus.  # noqa: E501
        :rtype: AudioStatus
        """
        return util.deserialize_model(dikt, cls)
