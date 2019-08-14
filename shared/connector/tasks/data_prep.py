from collections import namedtuple
from enum import IntEnum


class DataPrepTask(dict):
    """DataPrepTask is used for redis communication from API to DataPrepWorker

       The dict-type ensures that the class can be handled by the json
       package without special handling.
    """
    def __init__(self, training_id, resources, acoustic_model):
        dict.__init__(self,
                      training_id=training_id,
                      resources=resources,
                      acoustic_model=acoustic_model)

    @property
    def training_id(self):
        return self['training_id']

    @property
    def resources(self):
        return self['resources']

    @property
    def acoustic_model(self):
        return self['acoustic_model']


class DataPrepStatusCode(IntEnum):
    IN_PROGRESS = 10
    FAILURE = 100
    SUCCESS = 200


class DataPrepStatus(dict):
    """DataPrepStatus is used for redis communication from DataPrepWorker to API"""

    def __init__(self, id, training_id, message, __queue__='data_prep'):
        assert __queue__ == 'data_prep'

        dict.__init__(self, __queue__=__queue__,
                      id=int(id), message=message, training_id=training_id)

    @property
    def id(self):
        return DataPrepStatusCode(self['id'])

    @property
    def training_id(self):
        return self['training_id']

    @property
    def message(self):
        return self['message']
