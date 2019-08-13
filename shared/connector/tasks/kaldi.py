from collections import namedtuple
from enum import IntEnum


class KaldiTask(dict):
    """KaldiTask is used for redis communication from API to KaldiWorker

       The dict-type ensures that the class can be handled by the json
       package without special handling.
    """
    def __init__(self, acoustic_model, base_model, new_model):
        dict.__init__(self,
                      acoustic_model=acoustic_model,
                      base_model=base_model,
                      new_model=new_model)

    @property
    def acoustic_model(self):
        return self['acoustic_model']

    @property
    def base_model(self):
        return self['base_model']

    @property
    def new_model(self):
        return self['new_model']


class KaldiStatusCode(IntEnum):
    SUCCESS = 200


class KaldiStatus(dict):
    """KaldiStatus is used for redis communication from KaldiWorker to API"""

    def __init__(self, id, __queue__='kaldi'):
        assert __queue__ == 'kaldi'

        dict.__init__(self, __queue__=__queue__,
                      id=id)

    @property
    def id(self):
        return self['id']
