from collections import namedtuple
import json


KaldiTaskResource = namedtuple('TaskResource', ['corpus_path', 'dict_path'])


class KaldiTask:
    def __init__(self, base_path, target_path, resources):
        if not resources:
            resources = []

        self._base_path = base_path
        self._target_path = target_path
        self._resources = resources

    @property
    def base_path():
        return self._base_path

    @property
    def base_bucket():
        return '/'.join(self._base_path.split('/')[:-1])

    @property
    def base_object():
        return self._base_path.split('/')[-1]

    @property
    def target_path():
        return self.target_path

    @property
    def target_bucket():
        return '/'.join(self._target_path.split('/')[:-1])

    @property
    def target_object():
        return self._target_path.split('/')[-1]

    @property
    def resources():
        return self._resources

    def add_resource(resource):
        assert isinstance(resource, KaldiTaskResource)
        self._resources.append(resource)

    @staticmethod
    def toJSON():
        return json.dumps({
            'base_path': self._base_path,
            'target_path': self._target_path,
            'resources': [{
                'corpus_path': r.corpus_path,
                'dict_path': r.dict_path
                } for r in self._resources]
        })

    @staticmethod
    def fromJSON(json_str):
        json_obj = json.loads(json_str)

        self._base_path = json_obj['base_path']
        self._target_path = json_obj['target_path']

        self._resources = [KaldiTaskResource(
            corpus_path=r['corpus_path'],
            dict_path=r['dict_path']
            ) for r in json_obj['resources']]
