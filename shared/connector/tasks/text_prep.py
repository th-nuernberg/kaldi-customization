from collections import namedtuple
from enum import IntEnum


class TextPrepTask(dict):
    """TextPrepTask is used for redis communication from API to TextPrepWorker

       The dict-type ensures that the class can be handled by the json
       package without special handling.
    """
    def __init__(self, resource_uuid, file_type):
        dict.__init__(self,
                      resource_uuid=resource_uuid,
                      file_type=file_type)

    @property
    def resource_uuid(self):
        return self['resource_uuid']

    @property
    def file_type(self):
        return self['file_type']


class TextPrepStatusCode(IntEnum):
    IN_PROGRESS = 10
    FAILURE = 100
    SUCCESS = 200


class TextPrepStatus(dict):
    """TextPrepStatus is used for redis communication from TextPrepWorker to API"""

    def __init__(self, id, resource_uuid, message, __queue__='text_prep'):
        assert __queue__ == 'text_prep'

        dict.__init__(self, __queue__=__queue__,
                      id=id, message=message, resource_uuid=resource_uuid)

    @property
    def id(self):
        return self['id']

    @property
    def resource_uuid(self):
        return self['resource_uuid']

    @property
    def message(self):
        return self['message']
