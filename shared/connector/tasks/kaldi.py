from collections import namedtuple
from enum import IntEnum


class KaldiTask(dict):
    """KaldiTask is used for redis communication from API to KaldiWorker

       The dict-type ensures that the class can be handled by the json
       package without special handling.
    """
    def __init__(self, acoustic_model_id, training_id):
        dict.__init__(self,
                      acoustic_model_id=acoustic_model_id,
                      training_id=training_id)

    @property
    def acoustic_model_id(self):
        return self['acoustic_model_id']

    @property
    def training_id(self):
        return self['training_id']


class KaldiStatusCode(IntEnum):
    IN_PROGRESS = 10
    FAILURE = 100
    SUCCESS = 200


class KaldiStatus(dict):
    """KaldiStatus is used for redis communication from KaldiWorker to API"""

    def __init__(self, id, training_id, __queue__='kaldi'):
        assert __queue__ == 'kaldi'

        dict.__init__(self, __queue__=__queue__,
                      id=id, training_id=training_id)

    @property
    def id(self):
        return self['id']

    @property
    def training_id(self):
        return self['training_id']
