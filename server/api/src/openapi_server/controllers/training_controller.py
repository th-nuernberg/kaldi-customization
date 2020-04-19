import connexion
import six
import tempfile

from openapi_server.models.callback_object import CallbackObject  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.resource_reference_object import ResourceReferenceObject  # noqa: E501
from openapi_server.models.training import Training  # noqa: E501
from openapi_server import util

from models import db
from models.project import Project as DB_Project
from models.user import User as DB_User
from models.acousticmodel import AcousticModel as DB_AcousticModel
from models.resource import Resource as DB_Resource, ResourceStateEnum as DB_ResourceStateEnum
from models.training import Training as DB_Training, TrainingStateEnum as DB_TrainingStateEnum
from models.training_resource import TrainingResource as DB_TrainingResource
from models.resource import ResourceTypeEnum as DB_ResourceType

from redis_communication import create_dataprep_job, create_kaldi_job
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets, copy_object_in_bucket
from config import minio_client

import os
import json
from mapper import mapper
from flask import stream_with_context, Response

import re


def get_db_project_training(project_uuid, training_version):
    """
    Queries the database and returns the specified project / training.
    Returns None if not found
    """
    current_user = connexion.context['token_info']['user']

    db_proj = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()
    if db_proj is None:
        return None, None

    db_train = DB_Training.query.filter_by(
        project=db_proj,
        version=training_version).first()

    return db_proj, db_train


def assign_resource_to_training(project_uuid, training_version, resource_reference_object=None):  # noqa: E501
    """Assign a resource to the training

    Assign the specified resource to the training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_reference_object: Resource that needs to be added
    :type resource_reference_object: dict | bytes

    :rtype: Resource
    """
    if connexion.request.is_json:
        resource_reference_object = ResourceReferenceObject.from_dict(connexion.request.get_json())  # noqa: E501

    current_user = connexion.context['token_info']['user']

    db_proj = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if not db_proj:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(
        project_id=db_proj.id, version=training_version).first()

    if not db_training:
        return ("Training not found", 404)

    if not db_training.can_assign_resource():
        return ("Training already in progress", 400)

    db_resource = DB_Resource.query.filter_by(
        uuid=resource_reference_object.resource_uuid, owner_id=current_user.id).first()

    if not db_resource:
        return ("Resource not found", 404)

    if db_resource.has_error():
        return ("Resource has errors", 400)

    # if the resource is already added, return the previous
    db_training_resource = DB_TrainingResource.query.filter_by(
        training_id=db_training.id, origin_id=db_resource.id).first()
    if db_training_resource:
        return mapper.db_training_resource_to_front(db_training_resource)

    db_training_resource = DB_TrainingResource(
        training=db_training, origin=db_resource)
    db.session.add(db_training_resource)
    db.session.commit()

    # if text prep is already done, we should copy corpus to the new training_resource
    if db_resource.status == DB_ResourceStateEnum.TextPreparation_Success:
        copy_object_in_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], db_resource.uuid + "/corpus.txt",
                              minio_buckets["TRAINING_RESOURCE_BUCKET"], str(db_training_resource.id) + "/corpus.txt")

    if db_resource.status != DB_ResourceStateEnum.TextPreparation_Success:
        db_training.status = DB_TrainingStateEnum.TextPrep_Pending
    elif db_training.status == DB_TrainingStateEnum.Init:
        db_training.status = DB_TrainingStateEnum.Trainable

    db.session.add(db_training)
    db.session.commit()

    return mapper.db_training_resource_to_front(db_training_resource)


def create_training(project_uuid):  # noqa: E501
    """Create a new training

     # noqa: E501

    :param project_uuid: Project object that needs to be trained
    :type project_uuid: 

    :rtype: Training
    """
    current_user = connexion.context['token_info']['user']

    print(current_user)

    db_proj = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if (db_proj is None):
        return ("Project not found", 404)

    db_last_training = DB_Training.query.filter_by(
        project_id=db_proj.id).order_by(DB_Training.version.desc()).first()

    version = db_last_training.version + 1 if db_last_training else 1

    db_training = DB_Training(
        project=db_proj,
        version=version
    )
    db.session.add(db_training)
    db.session.commit()

    if db_last_training:
        #copy all resource files from last training
        db_last_training_resources = DB_TrainingResource.query.filter_by(training_id=db_last_training.id).all()

        has_pending_resources = False

        for tr in db_last_training_resources:
            db_training_resource = DB_TrainingResource(training=db_training,origin=tr.origin)
            db.session.add(db_training_resource)
            db.session.commit()
            if tr.origin.status == DB_ResourceStateEnum.TextPreparation_Success:
                copy_object_in_bucket(minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], str(tr.id) + "/corpus.txt",
                    minio_buckets["TRAINING_RESOURCE_BUCKET"], str(db_training_resource.id) + "/corpus.txt")
            else:
                has_pending_resources = True
            
        if has_pending_resources:
            db_training.status = DB_TrainingStateEnum.TextPrep_Pending
            db.session.add(db_training)
            db.session.commit()
    else:
        #copy base corpus
        db_resource = DB_Resource(
            status=DB_ResourceStateEnum.TextPreparation_Success,
            resource_type=DB_ResourceType.txt,
            owner=current_user,
            name="PROJ_" + str(db_proj.name) + "_ORIGINAL_CORPUS.txt"
        )

        db.session.add(db_resource)
        db.session.commit()

        db_training_resource = DB_TrainingResource(training=db_training,origin=db_resource)
        db.session.add(db_training_resource)
        db.session.commit()

        #copy base Corpus to Resource Bucket twice, since it is an txt file corpus = source
        copy_object_in_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(db_proj.acoustic_model_id) + "/corpus.txt",
            minio_buckets["RESOURCE_BUCKET"], str(db_resource.uuid) + "/source")
        copy_object_in_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(db_proj.acoustic_model_id) + "/corpus.txt",
            minio_buckets["RESOURCE_BUCKET"], str(db_resource.uuid) + "/corpus.txt")

        #also copy it to the training_resource bucket
        copy_object_in_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(db_proj.acoustic_model_id) + "/corpus.txt",
            minio_buckets["TRAINING_RESOURCE_BUCKET"], str(db_training_resource.id) + "/corpus.txt")

    return (mapper.db_training_to_front(db_training),201)


def delete_assigned_resource_from_training(project_uuid, training_version, resource_uuid):  # noqa: E501
    """Remove a resource from the training

    Removes the assigned resource from the training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid: 

    :rtype: None
    """
    current_user = connexion.context['token_info']['user']

    db_res = DB_Resource.query.filter_by(
        uuid=resource_uuid, owner_id=current_user.id).first()
    if db_res is None:
        return ("Resource not found", 404)

    db_proj, db_train = get_db_project_training(project_uuid, training_version)
    if db_proj is None:
        return ("Project not found", 404)
    if db_train is None:
        return ("Training not found", 404)

    # check if training already started
    if not db_train.can_assign_resource():
        return ("Conflict: already in training", 409)

    # check if already assigned
    db_train_res = DB_TrainingResource.query.filter_by(
        training=db_train,
        origin=db_res).first()

    if db_train_res is None:
        return ("Resource was not in training", 400)

    db.session.delete(db_train_res)
    db.session.commit()

    return ("Resource assignment successfully removed", 200)

def download_model_for_training(project_uuid, training_version):  # noqa: E501
    """Returns the model

    Returns the model of the specified training # noqa: E501

    :param project_uuid: UUID of project
    :type project_uuid: str
    :param training_version: Version of training
    :type training_version: int

    :rtype: file
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()

    if not db_project:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version,project_id=db_project.id).first()

    if not db_training:
        return ("Training not found", 404)

    status, stream = download_from_bucket(minio_client,
        bucket=minio_buckets["TRAINING_BUCKET"],
        filename='{}/graph.zip'.format(db_training.id)
    )

    if not status:  # means no success
        return ("File not found", 404)

    response = Response(response=stream, content_type="application/zip", direct_passthrough=True)
    response.headers['Content-Disposition'] = 'attachment; filename=graph.zip'
    return response

def get_corpus_of_training(project_uuid, training_version):  # noqa: E501
    """Get the entire corpus of the specified training

    Returns the entire corpus of the specified training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: str
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()

    if not db_project:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version,project_id=db_project.id).first()

    if not db_training:
        return ("Training not found", 404)

    status, stream = download_from_bucket(minio_client,
        bucket=minio_buckets["TRAINING_BUCKET"], 
        filename="{}/corpus.txt".format(db_training.id)
    )

    if not status:  # means no success
        return ("File not found", 404)

    return stream.read().decode('utf-8')

def get_corpus_of_training_resource(project_uuid, training_version, resource_uuid):  # noqa: E501
    """Get the corpus of the resource

    Returns the corpus of the specified resource for this training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid: 

    :rtype: str
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    db_resource = DB_Resource.query.filter(
        DB_Resource.uuid == resource_uuid).first()

    if db_resource is None:
        return ("Resource not found", 404)

    db_training_resource = DB_TrainingResource.query.filter_by(origin_id=db_resource.id) \
        .filter_by(training_id=db_training.id).first()

    if db_training_resource is None:
        return ("Resource not assigned to this Training", 404)

    status, stream = download_from_bucket(
        minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], "{}/corpus.txt".format(db_training_resource.id))

    print(db_training_resource.id)
    return stream.read().decode('utf-8') if status else ""


def get_current_training_for_project(project_uuid):  # noqa: E501
    """Get current training

     # noqa: E501

    :param project_uuid: Get the current training for a specific project
    :type project_uuid: 

    :rtype: Training
    """
    return 'do some magic!'


def get_lexicon_of_training(project_uuid, training_version):  # noqa: E501
    """Get the entire lexicon of the specified training

    Returns the entire lexicon of the specified training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid:
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: List[List[str]]
    """

    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()

    if not db_project:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version, project_id=db_project.id).first()

    if not db_training:
        return ("Training not found", 404)

    status, stream = download_from_bucket(minio_client,
                                          bucket=minio_buckets["TRAINING_BUCKET"],
                                          filename="{}/lexicon.txt".format(db_training.id)
                                          )

    if not status:  # means no success
        return ("File not found", 404)

    entrys = stream.read().decode('utf-8').splitlines()
    lex = []
    for entry in entrys:
        # print(entry)
        lex.append(re.split(r'\t+', entry.rstrip('\t')))

    return lex


def get_lexicon_of_training_resource(project_uuid, training_version, resource_uuid):  # noqa: E501
    """Get the lexicon of the resource

    Returns the lexicon of the specified resource for this training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid:
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid:

    :rtype: List[List[str]]
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    db_resource = DB_Resource.query.filter(
        DB_Resource.uuid == resource_uuid).first()

    if db_resource is None:
        return ("Resource not found", 404)

    db_training_resource = DB_TrainingResource.query.filter_by(origin_id=db_resource.id) \
        .filter_by(training_id=db_training.id).first()

    if db_training_resource is None:
        return ("Resource not assigned to this Training", 404)

    status, stream = download_from_bucket(
        minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], "{}/lexicon.txt".format(db_training_resource.id))

    print(db_training_resource.id)

    entrys = stream.read().decode('utf-8').splitlines()
    lex = []
    for entry in entrys:
        # print(entry)
        lex.append(re.split(r'\t+', entry.rstrip('\t')))

    return lex if status else ""


def get_training_by_version(project_uuid, training_version):  # noqa: E501
    """Find project training results by UUID

    Returns the training object # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: Training
    """
    current_user = connexion.context['token_info']['user']

    db_proj = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if not db_proj:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(
        project_id=db_proj.id, version=training_version).first()

    if not db_training:
        return ("Training not found", 404)

    return mapper.db_training_to_front(db_training)

def get_trainings_for_project(project_uuid):  # noqa: E501
    """Lists all Trainings of a Project

     # noqa: E501

    :param project_uuid: Gets all trainings for a specific project
    :type project_uuid: 

    :rtype: List[Training]
    """
    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()

    if not db_project:
        return ("Project not found",404)

    db_trainings = DB_Training.query.filter_by(project_id=db_project.id).all()

    traininglist = list()

    for t in db_trainings:
        traininglist.append(mapper.db_training_to_front(t))
    return traininglist


def get_vocabulary_of_training(project_uuid, training_version):  # noqa: E501
    """Get the entire vocabulary of the specified training

    Returns the entire vocabulary of the specified training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: str
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    status, stream = download_from_bucket(
        minio_client, minio_buckets["TRAINING_BUCKET"], "{}/unique_word_list.txt".format(db_training.id))

    return stream.read().decode('utf-8') if status else ""


def prepare_training_by_version(project_uuid, training_version, callback_object=None):  # noqa: E501
    """Prepare the specified training

    Start the preparation process for the specified training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param callback_object: Callback to be executed after the operation ended
    :type callback_object: dict | bytes

    :rtype: Training
    """
    callback_json = "{}"
    try:
        if connexion.request.is_json:
            callback_object = CallbackObject.from_dict(connexion.request.get_json())  # noqa: E501
        cb = dict()
        cb["url"] = callback_object.url
        cb["method"] = callback_object.method
        callback_json = json.dumps(cb)

    except:
        callback_object = None
    
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ("Project not found",404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ("Training not found",404)

    if db_training.status == DB_TrainingStateEnum.Init:
        return ("training only initialized or no changed since last training", 400)

    if db_training.status != DB_TrainingStateEnum.Trainable:
        return ("training already done or pending", 400)

    db_training.status = DB_TrainingStateEnum.Training_DataPrep_Pending
    db_training_resources = DB_TrainingResource.query.filter(
    DB_TrainingResource.training_id == db_training.id).all()

    db_training.prepare_callback = callback_json

    db.session.add(db_training)
    db.session.commit()

    create_dataprep_job(
        acoustic_model_id=db_project.acoustic_model_id,
        corpi=[r.id for r in db_training_resources],
        training_id=db_training.id
    )

    return mapper.db_training_to_front(db_training)


def set_corpus_of_training_resource(project_uuid, training_version, resource_uuid, body):  # noqa: E501
    """Set the corpus of the resource

    Updates the corpus of the specified resource for this training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid: 
    :param body: New or updated corpus as plain text
    :type body: str

    :rtype: None
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    if db_training.status not in (DB_TrainingStateEnum.Init, DB_TrainingStateEnum.Trainable, DB_TrainingStateEnum.TextPrep_Pending, DB_TrainingStateEnum.TextPrep_Failure):
        return ("Training already started or done", 409)

    db_resource = DB_Resource.query.filter(
        DB_Resource.uuid == resource_uuid).first()

    if db_resource is None:
        return ("Resource not found", 404)

    db_training_resource = DB_TrainingResource.query.filter_by(origin_id=db_resource.id) \
        .filter_by(training_id=db_training.id).first()

    if db_training_resource is None:
        return ("Resource not assigned to this Training", 404)

    f = tempfile.NamedTemporaryFile()
    f.write(body)
    f.flush()

    upload_to_bucket(minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], str(
        db_training_resource.id) + "/corpus.txt", f.name)

    f.close()
    return ("Success", 200)


def set_lexicon_of_training_resource(project_uuid, training_version, resource_uuid, request_body):  # noqa: E501
    """Set the lexicon of the resource

    Updates the lexicon of the specified resource for this training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid:
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid:
    :param request_body: New or updated lexicon as array with string-pairs
    :type request_body: List[]

    :rtype: None
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    if db_training.status not in (
    DB_TrainingStateEnum.Init, DB_TrainingStateEnum.Trainable, DB_TrainingStateEnum.TextPrep_Pending,
    DB_TrainingStateEnum.TextPrep_Failure):
        return ("Training already started or done", 409)

    db_resource = DB_Resource.query.filter(
        DB_Resource.uuid == resource_uuid).first()

    if db_resource is None:
        return ("Resource not found", 404)

    db_training_resource = DB_TrainingResource.query.filter_by(origin_id=db_resource.id) \
        .filter_by(training_id=db_training.id).first()

    if db_training_resource is None:
        return ("Resource not assigned to this Training", 404)

    tmp = []
    for t in request_body:
        tmp.append("\t".join(t))
    lex = "\n".join(tmp)

    f = tempfile.NamedTemporaryFile()
    f.write(lex)
    f.flush()

    upload_to_bucket(minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], str(
        db_training_resource.id) + "/lexicon.txt", f.name)

    f.close()
    return ("Success", 200)


def start_training_by_version(project_uuid, training_version, callback_object=None):  # noqa: E501
    """Start the specified training

    Start the training process for the specified training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param callback_object: Callback to be executed after the operation ended
    :type callback_object: dict | bytes

    :rtype: Training
    """
    callback_json = "{}"
    try:
        if connexion.request.is_json:
            callback_object = CallbackObject.from_dict(connexion.request.get_json())  # noqa: E501
        cb = dict()
        cb["url"] = callback_object.url
        cb["method"] = callback_object.method
        callback_json = json.dumps(cb)

    except:
        callback_object = None
        
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if not db_project:
        return ("Project not found",404)

    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if not db_training:
        return ("Training not found",404)

    if db_training.status == DB_TrainingStateEnum.Training_DataPrep_Success:
        db_training.train_callback = callback_json
        db_training.status = DB_TrainingStateEnum.Training_Pending
        db.session.add(db_training)
        db.session.commit()

        create_kaldi_job(
            training_id=db_training.id,
            acoustic_model_id=db_training.project.acoustic_model_id)
        return mapper.db_training_to_front(db_training)
    else:
        return ("Training already done or pending", 400)
