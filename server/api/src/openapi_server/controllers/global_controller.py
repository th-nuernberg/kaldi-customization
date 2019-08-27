import connexion
import six

from openapi_server.models.acoustic_model import AcousticModel  # noqa: E501
from openapi_server.models.language import Language  # noqa: E501
from openapi_server import util

from models.acousticmodel import AcousticModel as DB_AcousticModel
from models.language import Language as DB_Language

from mapper import mapper
from flask import stream_with_context, Response

from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets, copy_object_in_bucket
from config import minio_client

def download_acoustic_model(acoustic_model_uuid):  # noqa: E501
    """Returns the acoustic model

    Returns the model of the specified acoustic model # noqa: E501

    :param acoustic_model_uuid: UUID of the acoustic model
    :type acoustic_model_uuid: str

    :rtype: file
    """
    db_acoustic_model = DB_AcousticModel.query.filter_by(uuid=acoustic_model_uuid).first()

    if not db_acoustic_model:
        return ("Acousticmodel not found", 404)

    status, stream = download_from_bucket(minio_client,
        bucket=minio_buckets["ACOUSTIC_MODELS_BUCKET"],
        filename='{}/model.zip'.format(db_acoustic_model.id)
    )

    if not status:  # means no success
        return ("File not found", 404)

    response = Response(response=stream, content_type="application/zip", direct_passthrough=True)
    response.headers['Content-Disposition'] = 'attachment; filename=graph.zip'
    return response


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
