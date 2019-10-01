import connexion
import six
from redis_communication import create_decode_job
import json
import os
import datetime

from openapi_server.models.audio import Audio  # noqa: E501
from openapi_server.models.audio_reference_object import AudioReferenceObject  # noqa: E501
from openapi_server.models.callback_object import CallbackObject  # noqa: E501
from openapi_server.models.decode_audio import DecodeAudio  # noqa: E501
from openapi_server.models.decode_session import DecodeSession  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server import util

from mapper import mapper

from models import db, Project as DB_Project, Training as DB_Training, Decoding as DB_Decoding, DecodingStateEnum as DB_DecodingStateEnum, AudioResource as DB_AudioResource, AudioStateEnum as DB_AudioStateEnum, DecodingAudio as DB_DecodingAudio

from werkzeug.utils import secure_filename

from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
from config import minio_client
from flask import stream_with_context, Response

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'

def get_current_db_decode_session(db_project,db_training):    
    db_decoding = DB_Decoding.query.filter_by(training_id=db_training.id, status=DB_DecodingStateEnum.Init).first()

    if not db_decoding:
        return ("No active decoding session", 404)
    
    return (db_decoding, 200)

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in ['wav']:
            return filetype
    return None


def assign_audio_to_current_session(project_uuid, training_version, audio_reference_object=None):  # noqa: E501
    """Assign Audio to decoding session

    Assign audio to current decoding session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param audio_reference_object: Audio that needs to be decoded
    :type audio_reference_object: dict | bytes

    :rtype: DecodeAudio
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

    if not db_audioresource:
        return ("Audio Resouce not found",404)

    db_decoding_audio = DB_DecodingAudio.query \
        .join(DB_Decoding, DB_Decoding.id == DB_DecodingAudio.decoding_id) \
        .filter(DB_Decoding.training_id == db_training.id) \
        .filter(DB_DecodingAudio.audioresource_id == db_audioresource.id) \
        .first()
    if db_decoding_audio:
        return ("Audio already in this training decoded",400)

    #get current session or send error
    session = get_current_db_decode_session(db_project,db_training)
    if (session[1] != 200):
        return session
    db_session = session[0]

    db_decode_audio = DB_DecodingAudio(
        audioresource_id=db_audioresource.id,
        decoding_id=db_session.id
    )
    db.session.add(db_decode_audio)
    db.session.commit()

    return DecodeAudio(transcripts=json.loads(db_decode_audio.transcripts),audio=mapper.db_audio_to_front(db_audioresource),session_uuid=db_session.uuid)


def create_decode_session(project_uuid, training_version):  # noqa: E501
    """Create a new decoding session

    Create a new decoding session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: DecodeSession
    """
    current_user = connexion.context['token_info']['user']
    
    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    #get current session or send error
    session = get_current_db_decode_session(db_project,db_training)
    if (session[1] == 200):
        return ("An active session already exists",400)
    
    db_session = DB_Decoding(
        training_id=db_training.id,
        status=DB_DecodingStateEnum.Init
    )
    db.session.add(db_session)
    db.session.commit()

    return (mapper.db_decoding_session_to_front(db_session),201)


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


def delete_decode_session(project_uuid, training_version):  # noqa: E501
    """Delete the decoding session

    Delete the active decoding session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: None
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    #get current session or send error
    session = get_current_db_decode_session(db_project,db_training)
    if (session[1] != 200):
        return session
    db_session = session[0]

    DB_DecodingAudio.query.filter_by(decoding_id=db_session.id).delete()
    DB_Decoding.query.filter_by(id=db_session.id).delete()
    db.session.commit()

    return ("Successfully deleted",200)


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


def get_all_decode_sessions(project_uuid, training_version):  # noqa: E501
    """Get the all sessions

    Get the current decode session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: List[DecodeSession]
    """
    current_user = connexion.context['token_info']['user']
    
    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_decodings = DB_Decoding.query.filter_by(training_id=db_training.id).all()

    session_list = list()
    for d in db_decodings:
        session_list.append(mapper.db_decoding_session_to_front(d))
    
    return (session_list, 200)


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


def get_current_decode_session(project_uuid, training_version):  # noqa: E501
    """Get the current session

    Get the current decode session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: DecodeSession
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    #get current session or send error
    session = get_current_db_decode_session(db_project,db_training)
    if (session[1] != 200):
        return session
    db_session = session[0]

    return (mapper.db_decoding_session_to_front(db_session),200)


def get_decode_result(project_uuid, training_version, audio_uuid):  # noqa: E501
    """Get the result of a decoding task

    Returns the result of a decoding task # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param audio_uuid: UUID of the audio
    :type audio_uuid: 

    :rtype: DecodeAudio
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_audio = DB_AudioResource.query.filter_by(uuid=audio_uuid).first()

    if not db_audio:
        return ('Audio not found', 404)

    db_decoding_audio = DB_DecodingAudio.query \
        .join(DB_Decoding, DB_Decoding.id == DB_DecodingAudio.decoding_id) \
        .filter(DB_Decoding.training_id == db_training.id) \
        .filter(DB_DecodingAudio.audioresource_id == db_audio.id) \
        .first()

    if not db_decoding_audio:
        return ('Decoding not found', 404)

    db_session = DB_Decoding.query.filter_by(id=db_decoding_audio.decoding_id).first()

    return DecodeAudio(transcripts=json.loads(db_decoding_audio.transcripts),audio=mapper.db_audio_to_front(db_audio),session_uuid=db_session.uuid)


def get_decode_session(project_uuid, training_version, session_uuid):  # noqa: E501
    """Get a decode session

    Gets a specified session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param session_uuid: UUID of the session
    :type session_uuid: 

    :rtype: DecodeSession
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_session = DB_Decoding.query.filter_by(training_id=db_training.id, uuid=session_uuid).first()
    
    if not db_session:
        return ('Session not found', 404)

    
    return (mapper.db_decoding_session_to_front(db_session),200)



def get_decodings(project_uuid, training_version):  # noqa: E501
    """List of all decodings

    Returns a list of all decodings for this training version # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: List[DecodeAudio]
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_decoding_audios = DB_DecodingAudio.query \
        .join(DB_Decoding, DB_Decoding.id == DB_DecodingAudio.decoding_id) \
        .filter(DB_Decoding.training_id == db_training.id) \
        .all()

    decodings = list()
    for da in db_decoding_audios:
        db_session = DB_Decoding.query.filter_by(id=da.decoding_id).first()
        db_audio = DB_AudioResource.query.filter_by(id=da.audioresource_id).first()
        decodings.append(
            DecodeAudio(transcripts=json.loads(da.transcripts),audio=mapper.db_audio_to_front(db_audio),session_uuid=db_session.uuid)
        )


    return decodings


def start_decode(project_uuid, training_version, session_uuid, callback_object=None):  # noqa: E501
    """Commits the decode session for decoding

    Enqueue the currently active session for decoding # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param session_uuid: UUID of the session
    :type session_uuid: 
    :param callback_object: Callbackobject that gets executed after process
    :type callback_object: dict | bytes

    :rtype: DecodeSession
    """
    current_user = connexion.context['token_info']['user']
    try:
        if connexion.request.is_json:
            callback_object = CallbackObject.from_dict(connexion.request.get_json())  # noqa: E501
    except: 
        callback_object = None

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_session = DB_Decoding.query.filter_by(training_id=db_training.id, uuid=session_uuid).first()
    
    if not db_session:
        return ('Session not found', 404)

    if(db_session.status != DB_DecodingStateEnum.Init):
        return ('Decoding already in progress or finished',400)

    db_decode_audios = DB_DecodingAudio.query.filter_by(decoding_id=db_session.id).all()

    audioresource_uuids = list()
    for da in db_decode_audios:
        audioresource_uuids.append(DB_AudioResource.query.filter_by(id=da.audioresource_id).first().uuid)
    # TODO check if files are ready for decoding

    create_decode_job(audio_uuids=audioresource_uuids,
                        acoustic_model_id=db_project.acoustic_model_id, training_id=db_training.id, decode_uuid=db_session.uuid)

    db_session.status = DB_DecodingStateEnum.Decoding_Pending
    db.session.add(db_session)
    db.session.commit()

    print('Created Decoding job: ' + str(db_session))
    return (mapper.db_decoding_session_to_front(db_session),202)


def unassign_audio_to_current_session(project_uuid, training_version, audio_uuid):  # noqa: E501
    """Unassign Audio to decoding session

    Unassign audio to current decoding session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param audio_uuid: UUID of the audio
    :type audio_uuid: 

    :rtype: None
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ('Project not found', 404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ('Training not found', 404)

    db_audio = DB_AudioResource.query.filter_by(uuid=audio_uuid).first()

    if not db_audio:
        return ("Audio not found", 404)

    #get current session or send error
    session = get_current_db_decode_session(db_project,db_training)
    if (session[1] != 200):
        return session
    db_session = session[0] 

    db_decode_audio = DB_DecodingAudio.query.filter_by(audioresource_id=db_audio.id, decoding_id=db_session.id).first()
    if not db_decode_audio:
        return("Audio not in current decoding Session",404)
    
    DB_DecodingAudio.query.filter_by(audioresource_id=db_audio.id, decoding_id=db_session.id).delete()
    db.session.commit()

    return ("Successfully deleted", 200)


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
