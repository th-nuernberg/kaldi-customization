import connexion
import six
from redis_communication import create_decode_job
import json
import os
import datetime

from openapi_server.models.audio import Audio  # noqa: E501
from openapi_server.models.audio_reference_object import AudioReferenceObject  # noqa: E501
from openapi_server.models.audio_reference_with_callback_object import AudioReferenceWithCallbackObject  # noqa: E501
from openapi_server.models.binary_resource_object import BinaryResourceObject  # noqa: E501
from openapi_server.models.decode_message import DecodeMessage  # noqa: E501
from openapi_server.models.decode_task_reference import DecodeTaskReference  # noqa: E501
from openapi_server import util

from mapper import mapper

from models import db, Project as DB_Project, Training as DB_Training, Decoding as DB_Decoding, DecodingStateEnum as DB_DecodingStateEnum, AudioResource as DB_AudioResource, AudioStateEnum as DB_AudioStateEnum

from werkzeug.utils import secure_filename

from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
from config import minio_client
from flask import stream_with_context, Response

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'


def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return None


def assign_audio_to_training(project_uuid, training_version, audio_reference_object=None):  # noqa: E501
    """Assign Audio to training

    Assign audio to to be decoded in a specific training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param audio_reference_object: Audio that needs to be decoded
    :type audio_reference_object: dict | bytes

    :rtype: DecodeTaskReference
    """
    current_user = connexion.context['token_info']['user']

    if connexion.request.is_json:
        audio_reference_object = AudioReferenceObject.from_dict(connexion.request.get_json())  # noqa: E501

    # if user does not select file, browser also
    # submit an empty part without filename
    if audio_reference_object is None:
        return ('Invalid input', 405)
    
    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_audioresource = DB_AudioResource.query.filter_by(uuid=audio_reference_object.audio_uuid).first()

    db_decode = DB_Decoding(
        training=db_training,
        status=DB_DecodingStateEnum.Init,
        audioresource_id=db_audioresource.id
    )
    db.session.add(db_decode)
    db.session.commit()

    print('Added database entry: ' + str(db_decode))

    minio_file_path = str(db_audioresource.uuid)

    db.session.add(db_decode)
    db.session.commit()

    return DecodeTaskReference(decode_uuid=db_decode.uuid)

def delete_audio_by_uuid(audio_uuid):  # noqa: E501
    """Delete audio by UUID

    Delete a single audio resource # noqa: E501

    :param audio_uuid: UUID of audio to delete
    :type audio_uuid: str

    :rtype: None
    """
    audioresource = DB_AudioResource.query.filter_by(uuid=audio_uuid).first()

    if audioresource is None:
        return("Audio not found",404)
    
    #delete all referenced decodings
    DB_Decoding.query.filter_by(audioresource_id=audioresource.id).delete()
    DB_AudioResource.query.filter_by(uuid=audio_uuid).delete()
    db.session.commit()

    return ('Success',200)

def get_all_audio():  # noqa: E501
    """Returns a list of available audio

     # noqa: E501


    :rtype: List[Audio]
    """
    audioresources = DB_AudioResource.query.all()
    audiolist = list()
    for ar in audioresources:
        audiolist.append(mapper.db_audio_to_front(ar))
    return audiolist


def get_audio_by_uuid(audio_uuid):  # noqa: E501
    """Find audio by UUID

    Returns a single audio resource # noqa: E501

    :param audio_uuid: UUID of audio to return
    :type audio_uuid: str

    :rtype: Audio
    """
    audioresource = DB_AudioResource.query.filter_by(uuid=audio_uuid).first()

    if audioresource is None:
        return("Audio not found",404)

    return (mapper.db_audio_to_front(audioresource),200)


def get_audio_data(audio_uuid):  # noqa: E501
    """Returns the audio content

    Returns the audio content # noqa: E501

    :param audio_uuid: UUID of resource to return
    :type audio_uuid: str

    :rtype: file
    """
    current_user = connexion.context['token_info']['user']

    db_audio = DB_AudioResource.query.filter_by(uuid=audio_uuid).first()

    if not db_audio:
        return ("Audio not found", 404)

    status, stream = download_from_bucket(minio_client,
        bucket=minio_buckets["DECODING_BUCKET"],
        filename=db_audio.uuid
    )

    if not status:  # means no success
        print('audio {} in MinIO not found'.format(db_audio.uuid))
        return ("File not found", 404)

    response = Response(response=stream, content_type="audio/wav", direct_passthrough=True)
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(db_audio.name)
    return response


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
    current_user = connexion.context['token_info']['user']

    db_decoding = DB_Decoding.query \
        .join(DB_Training, DB_Training.id == DB_Decoding.training_id) \
        .join(DB_Project, DB_Training.project_id == DB_Project.id) \
        .filter(DB_Decoding.uuid == decode_uuid) \
        .filter(DB_Project.owner_id == current_user.id) \
        .first()

    if not db_decoding:
        return ('Decoding not found', 404)

    return DecodeMessage(uuid=db_decoding.uuid, transcripts=json.loads(db_decoding.transcripts))


def get_decodings(project_uuid, training_version):  # noqa: E501
    """List of all decodings

    Returns a list of all decodings for this training version # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: List[DecodeMessage]
    """
    current_user = connexion.context['token_info']['user']

    db_decodings = DB_Decoding.query \
        .join(DB_Training, DB_Training.id == DB_Decoding.training_id) \
        .join(DB_Project, DB_Training.project_id == DB_Project.id) \
        .filter(DB_Project.uuid == project_uuid) \
        .filter(DB_Project.owner_id == current_user.id) \
        .filter(DB_Training.version == training_version) \
        .all()

    decoding_list = list()

    for decoding in db_decodings:
        decoding_list.append(DecodeMessage(
            uuid=decoding.uuid, transcripts=json.loads(decoding.transcripts)))

    return decoding_list


def start_decode(project_uuid, training_version, decode_uuid, audio_reference_with_callback_object=None):  # noqa: E501
    """Decode audio to text

    Decode audio data to text using the trained project and the given audio # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param decode_uuid: UUID of the decoding task
    :type decode_uuid: 
    :param audio_reference_with_callback_object: Audio that needs to be decoded
    :type audio_reference_with_callback_object: dict | bytes

    :rtype: DecodeTaskReference
    """
    current_user = connexion.context['token_info']['user']

    if connexion.request.is_json:
        audio_reference_with_callback_object = AudioReferenceWithCallbackObject.from_dict(connexion.request.get_json())  # noqa: E501

    # if user does not select file, browser also
    # submit an empty part without filename
    if audio_reference_with_callback_object is None:
        return ('Invalid input', 405)

    print('Received new file for decode: ' + str(audio_reference_with_callback_object))
    
    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_audioresource = DB_AudioResource.query.filter_by(uuid=audio_reference_with_callback_object.audio_uuid).first()
    # TODO check if file is ready for decoding

    db_decode = DB_Decoding.query.filter_by(training_id=db_training.id,audioresource_id=db_audioresource.id).first()
    
    if(db_decode.status != DB_DecodingStateEnum.Init):
        return ('Decoding already in progress or finishd',400)


    minio_file_path = str(db_audioresource.uuid)

    create_decode_job(decode_file=minio_file_path,
                        acoustic_model_id=db_project.acoustic_model_id, training_id=db_training.id, decode_uuid=db_decode.uuid)

    db_decode.status = DB_DecodingStateEnum.Decoding_Pending
    db.session.add(db_decode)
    db.session.commit()

    print('Created Decoding job: ' + str(db_decode))

    return (DecodeTaskReference(decode_uuid=db_decode.uuid),202)

def upload_audio(upfile):  # noqa: E501
    """Uploads audio

     # noqa: E501

    :param upfile: File object that needs to be uploaded
    :type upfile: str

    :rtype: List[Audio]
    """

    filename = secure_filename(upfile.filename)
    filetype = get_filetype(filename)

    if filetype is None:
        return ('Invalid input', 405)

    db_audioresource = DB_AudioResource(
        name=filename
    )
    db.session.add(db_audioresource)
    db.session.commit()

    # cache file in local file system, then upload to MinIO
    if not os.path.exists(TEMP_UPLOAD_FOLDER):
        os.makedirs(TEMP_UPLOAD_FOLDER)

    local_file_path = os.path.join(TEMP_UPLOAD_FOLDER, str(db_audioresource.uuid))
    upfile.save(local_file_path)

    minio_file_path = str(db_audioresource.uuid)

    upload_result = upload_to_bucket(
        minio_client=minio_client,
        bucket=minio_buckets["DECODING_BUCKET"],
        filename=minio_file_path,
        file_path=local_file_path
    )

    # TODO: delete local file local_file_path

    if upload_result[0]:
        # TODO WRONG STATUS UNTIL AUDIO PREP WORKFLOW EXISTS
        db_audioresource.status = DB_AudioStateEnum.AudioPrep_Success
    else:
        db_audioresource.status = DB_AudioStateEnum.AudioPrep_Failure

    db.session.add(db_audioresource)
    db.session.commit()

    print('Uploaded audio file to MinIO: ' + str(db_audioresource))
    print(mapper.db_audio_to_front(db_audioresource))
    return (mapper.db_audio_to_front(db_audioresource),201)
