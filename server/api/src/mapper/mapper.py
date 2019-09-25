from openapi_server.models.acoustic_model import AcousticModel
from openapi_server.models.acoustic_model_type import AcousticModelType
from openapi_server.models.project import Project
from openapi_server.models.training import Training
from openapi_server.models.training_status import TrainingStatus
from openapi_server.models.user import User
from openapi_server.models.language import Language
from openapi_server.models.resource import Resource
from openapi_server.models.resource_type import ResourceType
from openapi_server.models.resource_status import ResourceStatus
from openapi_server.models.audio import Audio
from openapi_server.models.audio_status import AudioStatus
from openapi_server.models.decode_session import DecodeSession
from openapi_server.models.decode_session_status import DecodeSessionStatus
from openapi_server.models.decode_audio import DecodeAudio

import json

from models import db, Project as DB_Project, TrainingStateEnum as DB_TrainingStateEnum, User as DB_User, AcousticModel as DB_AcousticModel, DecodingAudio as DB_DecodingAudio, AudioResource as DB_AudioResource
from models.training_resource import TrainingResource as DB_TrainingResource
from models.training import Training as DB_Training

def db_project_to_front(db_project):
    if db_project.parent:
        parent_uuid = db_project.parent.uuid
    else:
        parent_uuid = None

    #TODO filter by user?
    trainings = DB_Training.query.filter_by(project=db_project).all()

    if trainings:
        training_list = [ db_training_to_front(t) for t in trainings ]
    else:
        training_list = []

    return Project(
        name=db_project.name,
        uuid=db_project.uuid,
        acoustic_model=db_acousticModel_to_front(db_project.acoustic_model),
        parent=parent_uuid,
        trainings=training_list,
        creation_timestamp=db_project.creation_timestamp,
        owner=db_user_to_front(db_project.owner)
    )

def db_acousticModel_to_front(db_acousticModel):
    return AcousticModel(
        uuid=db_acousticModel.uuid,
        name=db_acousticModel.name,
        language=db_language_to_front(db_acousticModel.language),
        model_type=AcousticModelTypeEnum_to_AcousticModelType(db_acousticModel.model_type)
    )

def db_user_to_front(db_user):
    return User(
        username=db_user.username,
        email=db_user.user_email
    )

def db_language_to_front(db_language):
    return Language(
        id=db_language.id,
        name=db_language.name
    )

def db_resource_to_front(db_resource):
    return Resource(
        name=db_resource.name,
        status=ResourceStateEnum_to_ResourceStatus(db_resource.status),
        resource_type=ResourceTypeEnum_to_ResourceType(db_resource.resource_type),
        uuid=db_resource.uuid,
        creation_timestamp=db_resource.upload_date
    )

def db_training_to_front(db_training):
    # TODO filter by user?
    resources = DB_TrainingResource.query.filter_by(training=db_training).all()

    if resources:
        resource_list = [db_training_resource_to_front(r) for r in resources]
    else:
        resource_list = []

    return Training(
        version=db_training.version,
        creation_timestamp=db_training.creation_timestamp,
        status=TrainingStateEnum_to_TrainingStatus(db_training.status),
        resources=resource_list
    )

def db_audio_to_front(db_audio):
    return Audio(
        uuid=db_audio.uuid,
        name=db_audio.name,
        creation_timestamp=db_audio.upload_date,
        status=AudioStateEnum_to_AudioStatus(db_audio.status)
    )

def db_decoding_session_to_front(db_decoding):
    #get all assignes decode audios
    decode_audios = DB_DecodingAudio.query.filter_by(decoding_id=db_decoding.id).all()
    decodings = list()
    for da in decode_audios:
        audio = DB_AudioResource.query.filter_by(id=da.audioresource_id).first()
        decodings.append(DecodeAudio(transcripts=json.loads(da.transcripts),audio=db_audio_to_front(audio),session_uuid=db_decoding.uuid))

    return DecodeSession(
        session_uuid=db_decoding.uuid,
        creation_timestamp=db_decoding.creation_timestamp,
        status=DecodingStateEnum_to_DecodingStatus(db_decoding.status),
        decodings=decodings
    )

def db_training_resource_to_front(db_training_resource):
    return db_resource_to_front(db_training_resource.origin)

def DecodingStateEnum_to_DecodingStatus(decodingState):
    return {
        100: DecodeSessionStatus.Init,
        150: DecodeSessionStatus.Decoding_Pending,
        200: DecodeSessionStatus.Decoding_InProgress,
        300: DecodeSessionStatus.Decoding_Success,
        320: DecodeSessionStatus.Decoding_Failure
        }[decodingState]

def ResourceTypeEnum_to_ResourceType(resourceType):
    return {
        1: ResourceType.html,
        2: ResourceType.docx,
        3: ResourceType.txt,
        4: ResourceType.pdf,
        5: ResourceType.png,
        6: ResourceType.jpg
        }[resourceType]

def ResourceStateEnum_to_ResourceStatus(resourceState):
    return {
        0: ResourceStatus.Upload_InProgress,
        1: ResourceStatus.Upload_Failure,
        9: ResourceStatus.TextPreparation_Ready,

        10: ResourceStatus.TextPreparation_Pending,
        11: ResourceStatus.TextPreparation_InProcess,
        12: ResourceStatus.TextPreparation_Failure,
        13: ResourceStatus.TextPreparation_Success
        }[resourceState]

def AcousticModelTypeEnum_to_AcousticModelType(modelType):
    return {
        100: AcousticModelType.HMM_GMM,
        200: AcousticModelType.HMM_DNN,
        300: AcousticModelType.HMM_RNN
        }[modelType]

def TrainingStateEnum_to_TrainingStatus(trainingState):
    return {
        100: TrainingStatus.Init,
        # text prep status missing
        150: TrainingStatus.TextPrep_Pending,
        151: TrainingStatus.TextPrep_Failure,
        200: TrainingStatus.Trainable,
        # data prep status missing
        205: TrainingStatus.Training_DataPrep_Pending,
        206: TrainingStatus.Training_DataPrep_InProgress,
        207: TrainingStatus.Training_DataPrep_Success,
        208: TrainingStatus.Training_DataPrep_Failure,
        210: TrainingStatus.Training_Pending,
        220: TrainingStatus.Training_In_Progress,
        300: TrainingStatus.Training_Success,
        320: TrainingStatus.Training_Failure
        }[trainingState]

def AudioStateEnum_to_AudioStatus(audioState):
    return {
        100: AudioStatus.Init,
        150: AudioStatus.AudioPrep_Pending,
        200: AudioStatus.AudioPrep_In_Progress,
        300: AudioStatus.AudioPrep_Success,
        320: AudioStatus.AudioPrep_Success
        }[audioState]