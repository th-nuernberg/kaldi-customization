import connexion
import six

from openapi_server.models.acoustic_model import AcousticModel  # noqa: E501
from openapi_server.models.language import Language  # noqa: E501
from openapi_server import util

from models.acousticmodel import AcousticModel as DB_AcousticModel
from models.language import Language as DB_Language

from mapper import mapper

def get_acoustic_models():  # noqa: E501
    """Returns a list of available acoustic models

     # noqa: E501


    :rtype: List[AcousticModel]
    """

    db_acousticmodels = DB_AcousticModel.query.all()
    return [ mapper.db_acousticModel_to_front(model) for model in db_acousticmodels ]

def get_languages():  # noqa: E501
    """Returns a list of available languages

     # noqa: E501


    :rtype: List[Language]
    """

    db_languages = DB_Language.query.all()
    return [ mapper.db_language_to_front(lang) for lang in db_languages ]
