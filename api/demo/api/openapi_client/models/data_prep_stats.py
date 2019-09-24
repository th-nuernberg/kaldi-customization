# coding: utf-8

"""
    Kaldi Customization Server

    Kaldi Customization Server.  # noqa: E501

    The version of the OpenAPI document: 1.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class DataPrepStats(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'unique_words_count': 'int',
        'total_words_count': 'int',
        'lines_count': 'int',
        'files_count': 'int'
    }

    attribute_map = {
        'unique_words_count': 'unique_words_count',
        'total_words_count': 'total_words_count',
        'lines_count': 'lines_count',
        'files_count': 'files_count'
    }

    def __init__(self, unique_words_count=None, total_words_count=None, lines_count=None, files_count=None):  # noqa: E501
        """DataPrepStats - a model defined in OpenAPI"""  # noqa: E501

        self._unique_words_count = None
        self._total_words_count = None
        self._lines_count = None
        self._files_count = None
        self.discriminator = None

        if unique_words_count is not None:
            self.unique_words_count = unique_words_count
        if total_words_count is not None:
            self.total_words_count = total_words_count
        if lines_count is not None:
            self.lines_count = lines_count
        if files_count is not None:
            self.files_count = files_count

    @property
    def unique_words_count(self):
        """Gets the unique_words_count of this DataPrepStats.  # noqa: E501

        The number of unique words  # noqa: E501

        :return: The unique_words_count of this DataPrepStats.  # noqa: E501
        :rtype: int
        """
        return self._unique_words_count

    @unique_words_count.setter
    def unique_words_count(self, unique_words_count):
        """Sets the unique_words_count of this DataPrepStats.

        The number of unique words  # noqa: E501

        :param unique_words_count: The unique_words_count of this DataPrepStats.  # noqa: E501
        :type: int
        """

        self._unique_words_count = unique_words_count

    @property
    def total_words_count(self):
        """Gets the total_words_count of this DataPrepStats.  # noqa: E501

        The total number words  # noqa: E501

        :return: The total_words_count of this DataPrepStats.  # noqa: E501
        :rtype: int
        """
        return self._total_words_count

    @total_words_count.setter
    def total_words_count(self, total_words_count):
        """Sets the total_words_count of this DataPrepStats.

        The total number words  # noqa: E501

        :param total_words_count: The total_words_count of this DataPrepStats.  # noqa: E501
        :type: int
        """

        self._total_words_count = total_words_count

    @property
    def lines_count(self):
        """Gets the lines_count of this DataPrepStats.  # noqa: E501

        The number of processed lines  # noqa: E501

        :return: The lines_count of this DataPrepStats.  # noqa: E501
        :rtype: int
        """
        return self._lines_count

    @lines_count.setter
    def lines_count(self, lines_count):
        """Sets the lines_count of this DataPrepStats.

        The number of processed lines  # noqa: E501

        :param lines_count: The lines_count of this DataPrepStats.  # noqa: E501
        :type: int
        """

        self._lines_count = lines_count

    @property
    def files_count(self):
        """Gets the files_count of this DataPrepStats.  # noqa: E501

        The number of processed files  # noqa: E501

        :return: The files_count of this DataPrepStats.  # noqa: E501
        :rtype: int
        """
        return self._files_count

    @files_count.setter
    def files_count(self, files_count):
        """Sets the files_count of this DataPrepStats.

        The number of processed files  # noqa: E501

        :param files_count: The files_count of this DataPrepStats.  # noqa: E501
        :type: int
        """

        self._files_count = files_count

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DataPrepStats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
