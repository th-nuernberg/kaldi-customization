from collections import namedtuple


KaldiTaskResource = namedtuple('TaskResource', ['corpus_path', 'dict_path'])
KaldiTask = namedtuple('Task', ['base_path', 'target_path', 'resources'])
