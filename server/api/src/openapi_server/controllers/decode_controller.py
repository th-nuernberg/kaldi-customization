import connexion
import six
from redis_communication import create_decode_job
import json
import os
import datetime

from openapi_server.models.binary_decode_object import BinaryDecodeObject  # noqa: E501
from openapi_server.models.decode_message import DecodeMessage  # noqa: E501
from openapi_server.models.decode_task_reference import DecodeTaskReference  # noqa: E501
from openapi_server import util

from models import db, Project as DB_Project, Training as DB_Training, Decoding as DB_Decoding, DecodingStateEnum as DB_DecodingStateEnum

from werkzeug.utils import secure_filename

from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
from config import minio_client

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in DB_ResourceType.__members__:
            return DB_ResourceType[filetype]
    return None

def get_decode_result(project_uuid, training_version, decode_uuid):  # noqa: E501
    """Get the result of a decoding task

    Returns the result of a decoding task # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param decode_uuid: UUID of the decoding task
    :type decode_uuid: 

    :rtype: DecodeMessage
    """
    return 'do some magic!'


def get_decodings(project_uuid, training_version):  # noqa: E501
    """List of all decodings

    Returns a list of all decodings for this training version # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: List[DecodeMessage]
    """
    return 'do some magic!'


def start_decode(project_uuid, training_version, binary_decode_object):  # noqa: E501
    """Decode audio to text

    Decode audio data to text using the trained project # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param binary_decode_object: 
    :type binary_decode_object: dict | bytes

    :rtype: DecodeTaskReference
    """
    if connexion.request.is_json:
        binary_decode_object = BinaryDecodeObject.from_dict(connexion.request.get_json())  # noqa: E501

    audio_file = binary_decode_object.audio_file
    print('Received new file for decode: ' + str(audio_file))


    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()
    db_training = DB_Training.query.filter_by(version=training_version,project=db_project).first()

    # if user does not select file, browser also
    # submit an empty part without filename
    if audio_file is None:
        return ('Invalid input', 405)
    
    filename = secure_filename(audio_file.filename)
    filetype = get_filetype(filename)

    if filetype is None:
        return ('Invalid input', 405)
    
    # file is okay: create db entry, store to dfs and create decode job

    db_file = DB_Decoding(
        training = db_training,
        status = DB_DecodingStateEnum.Init,
        upload_date = datetime.datetime.now()
    )
    db.session.add(db_file)
    db.session.commit()

    print('Added database entry: ' + str(db_file))

    # cache file in local file system, then upload to MinIO
    if not os.path.exists(TEMP_UPLOAD_FOLDER):
        os.makedirs(TEMP_UPLOAD_FOLDER)

    local_file_path = os.path.join(TEMP_UPLOAD_FOLDER, str(db_file.uuid))
    audio_file.save(local_file_path)

    minio_file_path = str(db_file.uuid)

    upload_result = upload_to_bucket(
        minio_client=minio_client,
        bucket=minio_buckets["DECODING_BUCKET"],
        filename=minio_file_path,
        file_path=local_file_path
    )

    #TODO: delete local file local_file_path

    if upload_result[0]:
        db_file.status = DB_DecodingStateEnum.Init
    else:
        db_file.status = DB_DecodingStateEnum.Decoding_Failure

    db.session.add(db_file)
    db.session.commit()

    print('Uploaded file to MinIO for decoding: ' + str(db_file))

    if db_file.status == DB_DecodingStateEnum.Init:
        create_decode_job(decode_file=minio_file_path,acoustic_model_id=db_project.acoustic_model_id,training_id=db_training.id)

        db_file.status = DB_DecodingStateEnum.Queued
        db.session.add(db_file)
        db.session.commit()

        print('Created Decoding job: ' + str(db_file))

    return InlineResponse202(decode_uuid=db_file.uuid)
