from collections import namedtuple
from enum import IntEnum
import json


class KaldiTask:
    def __init__(self, acoustic_model, base_model, new_model):
        if not resources:
            resources = []

        self._acoustic_model = acoustic_model
        self._base_model = base_model
        self._new_model = new_model

    @property
    def acoustic_model(self):
        return self._acoustic_model

    @property
    def base_model(self):
        return self._base_model

    @property
    def new_model(self):
        return self._new_model

    def toJSON(self):
        return json.dumps({
            'acoustic_model': self._acoustic_model,
            'base_model': self._base_model,
            'new_model': self._new_model
        })

    @staticmethod
    def fromJSON(json_str):
        json_obj = json.loads(json_str)

        return KaldiTask(
            acoustic_model = json_obj['acoustic_model'],
            base_model = json_obj['base_model'],
            new_model = json_obj['new_model']
        )


class KaldiStatusCode(IntEnum):
    SUCCESS = 200


class KaldiStatus:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    def toJSON(self):
        return json.dumps({
            'id': self._id
        })

    @staticmethod
    def fromJSON(json_str):
        json_obj = json.loads(json_str)

        return KaldiStatus(json_obj['id'])
